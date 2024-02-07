from django.core.exceptions import ValidationError
from django.forms import Form
from django.forms import BaseFormSet
from django import forms
from web_app.forms import css_classes


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self,upload_request, *args, **kwargs):
        if upload_request.multiple_files is True:
            kwargs.setdefault("widget", MultipleFileInput(attrs={'hidden': True}))
        else:
            kwargs.setdefault("widget", forms.ClearableFileInput(attrs={'hidden': True}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class FileForm(Form):
    request_uuid = forms.CharField(widget=forms.HiddenInput())

    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Add a note to your upload...',
            'rows': 2,
            'class': css_classes.text_area + "text-sm",
        }),
        label='Note',
        help_text="""Add a note to clarify what you are uploading, if needed. Notes do not substitute the upload of the requested files.
                            """)

    def __init__(self, **kwargs):
        self.request_index = kwargs.pop('request_index')
        self.space = kwargs.pop('space')
        super().__init__(**kwargs)
        upload_request = self.space.requests.filter(is_active=True)[self.request_index]
        self.fields['files'] = MultipleFileField(upload_request=upload_request, label='Files', required=False)

        self.fields['request_uuid'].initial = upload_request.pk
        self.upload_request = upload_request
        if upload_request.file_types.exists():
            self.fields['files'].widget.attrs['accept'] = ','.join(upload_request.formatted_extensions)

    def clean_files(self):
        super().clean()
        files = self.cleaned_data.get('files')
        if files and self.upload_request.file_types.exists() is True:
            for file in files:
                extension = file.name.split('.')[-1]
                if (extension in self.upload_request.extensions) is False:
                    self.add_error('files', f'{file.name} has extension {extension}, which is not allowed.')
        return files


class BaseFileFormSet(BaseFormSet):
    def is_valid(self):
        result = super().is_valid()
        if result is False:
            return result
            # Check if at least one form has non-empty 'files'
        if any(form.cleaned_data.get('files') for form in self.forms):
            return True
        else:
            # Add an error message to the formset
            self.non_form_errors().append(ValidationError("You need to upload at least one file."))
            return False

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs["request_index"] = index
        return kwargs
