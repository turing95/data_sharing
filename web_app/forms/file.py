from django.core.exceptions import ValidationError
from django.forms import Form
from django.forms import BaseFormSet
from django import forms
from django.utils.text import format_lazy

from web_app.forms import css_classes
from django.utils.translation import gettext_lazy as _


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, upload_request, *args, **kwargs):
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
            'placeholder': _('Add a note to your upload...'),
            'rows': 2,
            'class': css_classes.text_area + "text-sm",
        }),
        label=_('Notes'),
        help_text=_("""Add a note to clarify what you are uploading, if needed. Notes do not substitute the upload of the requested files.
                            """))

    def __init__(self, **kwargs):
        self.request_index = kwargs.pop('request_index')
        self.request = kwargs.pop('request')
        super().__init__(**kwargs)
        upload_request = self.request.upload_requests.filter(is_active=True)[self.request_index]
        self.fields['files'] = MultipleFileField(upload_request=upload_request, label='Files', required=False)

        self.fields['request_uuid'].initial = upload_request.pk
        self.upload_request = upload_request

    def clean_files(self):
        super().clean()
        files = self.cleaned_data.get('files')

        # Ensure 'files' is always iterable
        if not isinstance(files, (list, tuple)):
            files = [files] if files else []
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
            self.non_form_errors().append(ValidationError(_("You need to upload at least one file.")))
            return False

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs["request_index"] = index
        return kwargs


class InputRequestForm(Form):
    request_uuid = forms.CharField(widget=forms.HiddenInput())

    def is_valid(self):
        result = super().is_valid()
        if result is False:
            return result
        if self.input_request.upload_request:
            if self.cleaned_data.get('files'):
                return True
            else:
                # Add an error message to the formset
                self.errors.append(ValidationError(_("You need to upload at least one file.")))
                return False
        return True

    def __init__(self, **kwargs):
        self.input_request_index = kwargs.pop('input_request_index')
        self.request = kwargs.pop('request')
        super().__init__(**kwargs)
        input_request = self.request.input_requests.all()[self.input_request_index]
        if input_request.upload_request:
            self.fields['files'] = MultipleFileField(upload_request=input_request.upload_request, label='Files',
                                                     required=False)
            self.fields['notes'] = forms.CharField(
                required=False,
                widget=forms.Textarea(attrs={
                    'placeholder': _('Add a note to your upload...'),
                    'rows': 2,
                    'class': css_classes.text_area + "text-sm",
                }),
                label=_('Notes'),
                help_text=_("""Add a note to clarify what you are uploading, if needed. Notes do not substitute the upload of the requested files.
                                """))
            self.fields['request_uuid'].initial = input_request.upload_request.pk
            self.upload_request = input_request.upload_request
        elif input_request.text_request:
            self.fields['text'] = forms.CharField(label=input_request.text_request.title, required=False,
                                                  widget=forms.Textarea(attrs={'rows': 2}))
            self.fields['request_uuid'].initial = input_request.text_request.pk
            self.text_request = input_request.text_request
        self.input_request = input_request


class BaseInputRequestFormSet(BaseFormSet):

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs["input_request_index"] = index
        return kwargs

    def is_valid(self):
        result = super().is_valid()
        return result
