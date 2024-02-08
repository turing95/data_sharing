import re
from django.forms import BaseInlineFormSet, inlineformset_factory, ModelForm
from django.core.exceptions import ValidationError
from web_app.models import Space, UploadRequest, FileType, GoogleDrive, OneDrive
from web_app.forms import css_classes
from django.urls import reverse_lazy
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

    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Untitled request*',
                                                          'required': 'required',
                                                          'class': css_classes.text_request_title_input}),
                            label='Request title - MANDATORY',
                            help_text="""This will be displayed to your invitees. Assign a meaningful title to your request to help your invitees understand what you are asking for.""")

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
                            label_off='Apply file restrictions',
                            attrs={
                                'onclick': 'toggleFileTypeRestrict(this)'
                            }),
        required=False,
        label='File Type Restrictions',
        help_text="""
                Only selected file types will be accepted. Leave blank to accept all file types.
            """)
    file_types = CommaSeparatedFileTypeField(
        widget=forms.HiddenInput(attrs={'class': 'file-types'}),
        label='File type restrictions',
        required=False)

    # DESTINATION FOLDER FIELDS
    # providers dropdown

    destination_type_select = forms.ChoiceField(
        choices=[
            (GoogleDrive.TAG, 'Google Drive'),
            (OneDrive.TAG, 'One Drive'),
        ],
        label="Destination folder",
        widget=forms.Select(
            attrs={'class': "bg-gray-50 border border-gray-300 text-gray-900 text-sm flex-grow w-full h-full",
                   'hx-trigger': "change, load",
                   'hx-get': reverse_lazy('select_destination_type'),
                   'hx-target': "previous .destination-search",
                   'hx-swap': "outerHTML"
                   })
    )

    destination_id = forms.CharField(
        widget=forms.HiddenInput(attrs={'class': 'destination'}),
        label="Destination folder ID",
        help_text="""The file uploaded for this request will be sent to the folder selected here. Choose a cloud storage provider and search for a folder and select it.""")

    destination_type = forms.CharField(widget=forms.HiddenInput(attrs={'class': 'destination-type'}),
                                       label="Destination type")

    destination_display = forms.CharField(
        required=False,
        label='Non-editable Field',
        widget=forms.TextInput(
            attrs={
                'class': ' w-full h-full px-2 py-1 text-base truncate focus:ring-0 focus:outline-none focus:border-0 bg-transparent border-none sm:text-sm' + ' destination-display',
                'readonly': 'readonly',
                'placeholder': 'No folder selected yet'
            }
        )
    )

    # REQUEST INSTRUCTIONS
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
        widget=ToggleWidget(label_on='Enable custom file names',
                            label_off='Enable custom file names',
                            attrs={
                                'onclick': 'toggleRename(this)'
                            }),
        required=False,
        label='File Naming',
        help_text="""
                By default, files are saved to your destination folder with the name they have been uploaded with.
                You can choose to apply a custom file name to add parametric information to the file names to make them more meaningful and standardized
            """)
    multiple_files = forms.BooleanField(
        widget=ToggleWidget(label_on='Allow multiple files upload',
                            label_off='Allow multiple files upload'),
        required=False,
        label='Multiple Files',
        help_text="""
                By default, each request can only contain one file. You can choose to enable multiple files upload for this request.
            """)

    class Meta:
        model = UploadRequest
        fields = ['title', 'file_naming_formula', 'instructions', 'multiple_files']

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        index = kwargs.pop('index', None)
        super().__init__(*args, **kwargs)
        self.fields['destination_type_select'].widget.attrs['hx-get'] += f'?next={request.get_full_path()}&request_index={index}'

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
        super().__init__(*args, **kwargs)
        if self.instance and UploadRequest.objects.filter(pk=self.instance.pk).exists():
            self.fields['uuid'].initial = self.instance.uuid

            destination = self.instance.destination
            if self.instance.file_naming_formula is not None:
                self.fields['rename'].initial = True
            self.fields['destination_id'].initial = destination.folder_id
            self.fields['destination_display'].initial = destination.name
            self.fields['destination_type'].initial = destination.tag
            self.fields['destination_type_select'].initial = destination.tag
            if self.instance.filetype_set.exists():
                self.fields['file_types'].initial = ','.join(
                    [file_type.slug for file_type in self.instance.filetype_set.all()])
                self.fields['file_type_restrict'].initial = True


class CustomInlineFormSet(BaseInlineFormSet):

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs["index"] = index
        return kwargs


RequestFormSet = inlineformset_factory(Space, UploadRequest, form=RequestForm, formset=CustomInlineFormSet, extra=1)
DetailRequestFormSet = inlineformset_factory(Space, UploadRequest, form=DetailRequestForm, formset=CustomInlineFormSet,
                                             extra=0)
