import re

from google.auth.exceptions import RefreshError
from django.forms import BaseInlineFormSet, inlineformset_factory, ModelForm
from django.core.exceptions import ValidationError
from web_app.models import Space, UploadRequest, FileType, GoogleDrive
from web_app.forms import css_classes
from django import forms
from django.utils.safestring import mark_safe
from web_app.forms.widgets import ToggleWidget, CustomCheckboxSelectMultiple


class FileTypeChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        # Return the string you want to display for each object
        return obj.slug


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

    file_types = FileTypeChoiceField(
        queryset=FileType.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={
            'onchange': 'handleCheckboxChange(this)',
        }),
        label='Restrict File Types',
        help_text=""" 
                Leave blank to allow all extensions to be uploaded or select specific file extensions to forbid all the others.
            """)

    class Meta:
        model = UploadRequest
        fields = ['title', 'file_types', 'file_naming_formula', 'instructions']

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
        file_types = cleaned_data.get('file_types', [])

        if file_type_restrict is False:
            # Uncheck all file types if the file_type_restrict is False
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
            
            if self.instance.file_types.exists():
                self.fields['file_type_restrict'].initial = True
                
            
            initial_file_types = self.instance.file_types.all()
            self.fields['file_types'].initial = initial_file_types
            # # Step 1: Fetch the related FileType instances from the current UploadRequest instance
            # related_file_types = self.instance.file_types.all()

            # # Step 2: Initialize an empty list to hold the primary keys
            # file_type_pks = []

            # # Step 2.1: Loop through each FileType instance
            # for file_type in related_file_types:
            #     # Step 2.2: Extract the primary key of the FileType instance
            #     file_type_pk = file_type.pk

            #     # Step 2.3: Add the primary key to the list
            #     file_type_pks.append(file_type_pk)

            #     # Debugging: Check the value of file_type_pk and ensure it's correct

            # # Step 3: Set the initial value of the 'file_types' field to the list of primary keys
            # self.fields['file_types'].initial = file_type_pks
            a=1



class UniqueTitleFormSet(BaseInlineFormSet):
    pass
    '''def clean(self):
        """
        Add validation to ensure that each request has a unique title within the set.
        """
        super().clean()

        # Skip further validation if any form already has errors
        if any(self.errors):
            return

        titles = set()
        for form in self.forms:
            # Ignore empty forms and forms marked for deletion
            if self.can_delete and self._should_delete_form(form):
                continue

            title = form.cleaned_data.get('title', None)
            if title and title in titles:
                raise ValidationError("Each request must have a unique title.")
            titles.add(title)'''


# Replace the standard formset with the custom one
RequestFormSet = inlineformset_factory(Space, UploadRequest, form=RequestForm, formset=UniqueTitleFormSet, extra=1)
DetailRequestFormSet = inlineformset_factory(Space, UploadRequest, form=DetailRequestForm, formset=UniqueTitleFormSet,
                                             extra=0)
