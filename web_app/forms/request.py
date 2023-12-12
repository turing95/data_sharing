from google.auth.exceptions import RefreshError
from django.forms import BaseInlineFormSet, inlineformset_factory, ModelForm
from django.core.exceptions import ValidationError
from web_app.models import Space, UploadRequest, FileType, GoogleDrive
from web_app.forms import css_classes
from django import forms
from django.utils.safestring import mark_safe


class FileTypeChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        # Return the string you want to display for each object
        return obj.extension


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
                            label='Request title')

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
                   'class': css_classes.text_input + ' cursor-not-allowed',
                   'onclick': 'handleAuthClick(this)'})
    )

    destination = forms.CharField(
        widget=forms.HiddenInput(),
        label="Destination folder")

    rename = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            'class': css_classes.checkbox_input,
            'onclick': 'toggleRename(this);'
        }),
        required=False,
        label='Apply custom file name'
    )

    file_types = FileTypeChoiceField(
        queryset=FileType.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,  # or any other suitable widget
        label='File Types',
        help_text='Select one or more file types.'
    )
    
  

    class Meta:
        model = UploadRequest
        fields = ['title', 'file_types', 'file_naming_formula', 'instructions']
        widgets = {
            'instructions': forms.Textarea(
                attrs={'placeholder': 'Add request-specific instructions here',
                       'rows': 3,
                       'class': css_classes.text_area,
                       'label': 'Instructions'}) 
        }

    def clean_file_naming_formula(self):
        file_naming_formula = self.cleaned_data.get('file_naming_formula')
        rename = self.cleaned_data.get('rename', False)

        if rename is False:
            file_naming_formula = None
        else:
            # List of valid tags
            valid_tags = [tag.label for tag in UploadRequest.FileNameTag]

            # Parsing the file_naming_formula for content in curly brackets
            invalid_tags = []
            start_index = file_naming_formula.find('{')
            while start_index != -1:
                end_index = file_naming_formula.find('}', start_index)
                if end_index == -1:
                    # No closing bracket found - break out of the loop
                    break

                # Extracting the tag
                tag = file_naming_formula[start_index + 1:end_index]
                if tag not in valid_tags:
                    invalid_tags.append(tag)

                # Update start_index for next iteration
                start_index = file_naming_formula.find('{', end_index)

            if invalid_tags:
                error_message = 'The following tags are not valid: ' + ', '.join(invalid_tags)
                raise forms.ValidationError(error_message)

        return file_naming_formula


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

            destination: GoogleDrive = self.instance.destinations.filter(tag=GoogleDrive.TAG).first().related_object
            if self.instance.file_naming_formula is not None:
                self.fields['rename'].initial = True
            self.fields['destination'].initial = destination.folder_id
            try:
                self.fields['destination_display'].initial = destination.name
            except RefreshError:
                self.fields['destination_display'].initial = "Error: refresh token"
            self.fields['file_types'].initial = [f.extension for f in self.instance.file_types.all()]


class UniqueTitleFormSet(BaseInlineFormSet):
    def clean(self):
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
            titles.add(title)


# Replace the standard formset with the custom one
RequestFormSet = inlineformset_factory(Space, UploadRequest, form=RequestForm, formset=UniqueTitleFormSet, extra=1)
DetailRequestFormSet = inlineformset_factory(Space, UploadRequest, form=DetailRequestForm, formset=UniqueTitleFormSet,
                                             extra=0)
