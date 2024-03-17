from django.forms import ModelForm
from django.urls import reverse_lazy

from web_app.forms import css_classes
from web_app.models import TextSection, FileSection
from django import forms
from django.utils.translation import gettext_lazy as _


class TextSectionForm(ModelForm):
    title = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': _('Untitled section'),
                                                                          'class': css_classes.text_request_title_input,
                                                                          'hx-trigger': 'blur changed',
                                                                          'hx-swap': 'none'}))

    class Meta:
        model = TextSection
        fields = ['title']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_url = reverse_lazy('text_section_update', kwargs={'text_section_uuid': self.instance.pk})
        self.fields['title'].widget.attrs['hx-post'] = update_url


class FileSectionForm(ModelForm):
    title = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': _('Untitled section'),
                                                                          'class': css_classes.text_request_title_input,
                                                                          'hx-target': 'closest .file-section-container'}))
    file = forms.FileField(required=False,
                           widget=forms.ClearableFileInput(attrs={'hx-encoding': 'multipart/form-data',
                                                                  'hx-target': 'closest .file-section-container'}))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': css_classes.text_area,
                                                                               'rows': 5,
                                                                               'cols': 5,
                                                                               'hx-target': 'closest .file-section-container'}))

    class Meta:
        model = FileSection
        fields = ['title', 'description']

    def clean_file(self):
        super().clean()
        file = self.cleaned_data.get('file')
        return file

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update_url = reverse_lazy('file_section_update', kwargs={'file_section_uuid': self.instance.pk})
        self.fields['title'].widget.attrs['hx-post'] = self.update_url
        self.fields['description'].widget.attrs['hx-post'] = self.update_url
        self.fields['file'].widget.attrs['hx-post'] = self.update_url
