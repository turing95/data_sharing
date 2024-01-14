import re

from google.auth.exceptions import RefreshError
from django.forms import BaseInlineFormSet, inlineformset_factory, ModelForm
from django.core.exceptions import ValidationError
from web_app.models import Space, UploadRequest, FileType, GoogleDrive
from web_app.forms import css_classes
from django import forms
from django.utils.safestring import mark_safe
from web_app.forms.widgets import ToggleWidget



class CommaSeparatedFileTypeField(forms.CharField):

    def to_python(self, value):
        if not value:
            return []
        file_types = []
        for slug in value.split(','):
            file_type = FileType.objects.filter(slug=slug).first()
            if file_type is None:
                raise ValidationError(f"{slug} is not a valid file type")
            file_types.append(file_type)
        return file_types


class RequestForm(ModelForm):
    instance: UploadRequest
    FILE_NAME_INSTRUCTIONS = "Name the file as you want it to appear in your destination folder. You can use tags to make the file name parametric. Here is the list of the possible tags:"
    FILE_NAME_TAGS = "<br>" + "<br>".join([
        f"- <strong>{{{tag[1]}}}</strong> - \"{'spiegazione va qui'}\""
        for tag in UploadRequest.FileNameTag.choices
    ])

    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Untitled request',
                                                          'required': 'required',
                                                          'class': css_classes.text_request_title_input}),
                            label='Request title',
                            help_text="""This will be displayed to your invitees.
                                """)

    # handling of the parametric file name
    file_naming_formula = forms.CharField(required=False,
                                          help_text=mark_safe(
                                              f"<div class='text-xs'>{FILE_NAME_INSTRUCTIONS}{FILE_NAME_TAGS}</div>"),
                                          widget=forms.TextInput(
                                              attrs={'placeholder': 'Insert file name, use tags for dynamic naming',
                                                     'class': "file-naming-formula placeholder-gray-500 my-1 min-h-[42px] min-h-32" + css_classes.text_input}),
                                          label='File naming formula')

    # Preparing the choices for the dropdown
    tag_choices = [(tag.label, tag.label) for tag in UploadRequest.FileNameTag]
    tag_choices.insert(0, ('', 'Insert parameter'))  # Add the default option

    # available tags dropdown
    available_tags_dropdown = forms.ChoiceField(
        choices=tag_choices,
        required=False,
        label='Available naming tags',
        widget=forms.Select(attrs={'class': css_classes.dropdown,
                                   'onchange': 'handleTagDropdownChange(this)'
                                   })
    )

    file_type_restrict = forms.BooleanField(
        widget=ToggleWidget(label_on='Apply file restrictions',
                            label_off='No file type restrictions',
                            attrs={
                                'onclick': 'toggleFileTypeRestrict(this)'
                            }),
        required=False,
        label='File Type Restrictions',
        help_text="""
                ...
            """)
    file_types = CommaSeparatedFileTypeField(
        widget=forms.HiddenInput(attrs={'class': 'file-types'}),
        label='File type restrictions',
        required=False)

    destination_display = forms.CharField(
        required=False,
        label='Non-editable Field',
        widget=forms.TextInput(
            attrs={'placeholder': 'Click to select a folder',
                   'class': css_classes.text_input + ' cursor-pointer',
                   'onclick': 'handleAuthClick(this)',
                   'readonly': 'readonly'})
    )

    destination = forms.CharField(
        widget=forms.HiddenInput(),
        label="Destination folder",
        help_text=
        """Select a destination folder from inside your cloud storage system. All files uploaded for this request will directly be uploaded to your selected folder.
            You will be able to change it at any time but be aware that this may lead to files uploaded for the same request to be in different folders  
            """)

    instructions = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Add request-specific instructions here',
            'rows': 2,
            'class': css_classes.text_area,
        }),
        label='Request Instructions',
        help_text="""Use this to provide additional information for your invitees that are specific to the request.
                                Leave blank if not necessary.
                            """)

    rename = forms.BooleanField(
        widget=ToggleWidget(label_on='Enabled custom file names',
                            label_off='Disabled custom file names',
                            attrs={
                                'onclick': 'toggleRename(this)'
                            }),
        required=False,
        label='File Naming',
        help_text="""
                By default, files are saved to your destination folder with the name they have been uploaded with.
                You can choose to apply a custom file name to add parametric information to the file names to make them more meaningful and standardized
            """)

    class Meta:
        model = UploadRequest
        fields = ['title', 'file_naming_formula', 'instructions']

    def clean_file_naming_formula(self):
        file_naming_formula = self.cleaned_data.get('file_naming_formula')
        valid_tags = [tag.label for tag in UploadRequest.FileNameTag]

        # Regular expression to find content within curly brackets
        regex_pattern = r"\{{([^}]+)\}}"
        found_tags = re.findall(regex_pattern, file_naming_formula)

        # Filtering out invalid tags
        invalid_tags = [tag for tag in found_tags if tag not in valid_tags]

        if invalid_tags:
            error_message = 'The following tags are not valid: ' + ', '.join(invalid_tags)
            self.add_error('file_naming_formula', error_message)

        return file_naming_formula

    def clean(self):
        cleaned_data = super().clean()
        rename = cleaned_data.get('rename', False)
        file_naming_formula = cleaned_data.get('file_naming_formula', None)
        if rename is False:
            cleaned_data['file_naming_formula'] = None
        else:
            if file_naming_formula is file_naming_formula is None or file_naming_formula == '':
                self.add_error('file_naming_formula', 'You must provide a file name if you want to rename the files.')

        file_type_restrict = cleaned_data.get('file_type_restrict', False)
        if file_type_restrict is False:
            cleaned_data['file_types'] = []
        return cleaned_data


class DetailRequestForm(RequestForm):
    uuid = forms.UUIDField(
        widget=forms.HiddenInput(),
    )

    def __init__(self, *args, **kwargs):
        # Manually include the uuid field
        self.access_token = kwargs.pop('access_token', None)
        super().__init__(*args, **kwargs)
        if self.instance and UploadRequest.objects.filter(pk=self.instance.pk).exists():
            self.fields['uuid'] = forms.CharField(
                widget=forms.HiddenInput()
            )
            self.fields['uuid'].initial = self.instance.uuid

            destination: GoogleDrive = self.instance.google_drive_destination
            if self.instance.file_naming_formula is not None:
                self.fields['rename'].initial = True
            self.fields['destination'].initial = destination.folder_id
            try:
                self.fields['destination_display'].initial = destination.name
            except RefreshError:
                self.fields['destination_display'].initial = "Error: refresh token"
            if self.instance.filetype_set.exists():
                self.fields['file_types'].initial = ','.join(
                    [file_type.slug for file_type in self.instance.filetype_set.all()])
                self.fields['file_type_restrict'].initial = True


# Replace the standard formset with the custom one
RequestFormSet = inlineformset_factory(Space, UploadRequest, form=RequestForm, formset=BaseInlineFormSet, extra=1)
DetailRequestFormSet = inlineformset_factory(Space, UploadRequest, form=DetailRequestForm, formset=BaseInlineFormSet,
                                             extra=0)
