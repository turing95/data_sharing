from django.forms import Form
from django.forms import BaseFormSet
from django import forms


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(attrs={'hidden': True,
                                                             'onchange': ' handleFilesUpload(this)'}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class FileForm(Form):
    files = MultipleFileField(label='Files')
    request_uuid = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, **kwargs):
        self.request_index = kwargs.pop('request_index')
        self.space = kwargs.pop('space')
        super().__init__(**kwargs)
        upload_request = self.space.requests.filter(is_deleted=False)[self.request_index]
        self.fields['request_uuid'].initial = upload_request.pk
        self.upload_request = upload_request
        if upload_request.file_types.exists():
            self.fields['files'].widget.attrs['accept'] = ','.join(upload_request.formatted_extensions)

    def clean_files(self):
        super().clean()
        files = self.cleaned_data.get('files')
        if self.upload_request.file_types.exists() is True:
            for file in files:
                extension = file.name.split('.')[-1]
                if (extension in self.upload_request.extensions) is False:
                    self.add_error('files', f'Extension {extension}  is not allowed.')
        return files


class BaseFileFormSet(BaseFormSet):
    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs["request_index"] = index
        return kwargs
