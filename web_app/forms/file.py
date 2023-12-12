from django.forms import Form
from django.forms import BaseFormSet
from django import forms


class FileForm(Form):
    file = forms.FileField(label='File')
    request_uuid = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, **kwargs):
        self.request_index = kwargs.pop('request_index')
        self.space = kwargs.pop('space')
        super().__init__(**kwargs)
        self.fields['request_uuid'].initial = self.space.requests.all()[self.request_index].uuid


class BaseFileFormSet(BaseFormSet):
    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs["request_index"] = index
        return kwargs
