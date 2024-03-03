from django import forms

from web_app.forms import css_classes
from web_app.models import File
from django.utils.translation import gettext_lazy as _
            
class MultipleFileField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj


class FileSelectForm(forms.Form):
    files = MultipleFileField(
        queryset=None,  # This will be dynamically set based on the sender_event
        widget=forms.CheckboxSelectMultiple(attrs={'class': css_classes.checkbox_input}),
    )
    notes = forms.CharField(
        widget=forms.Textarea(attrs={'class': css_classes.text_area,
                                     'rows': 5,
                                     'cols': 5}),
        required=False,
    )

    def clean_files(self):
        if not self.cleaned_data['files']:
            raise forms.ValidationError(_("You must select at least one file"))
        return self.cleaned_data['files']

    def __init__(self, *args, **kwargs):
        sender = kwargs.pop('sender', None)
        upload_request = kwargs.pop('upload_request', None)
        public = kwargs.pop('public', None)
        super().__init__(*args, **kwargs)
        if upload_request:
            queryset = File.objects.filter(sender_event__request=upload_request)
            if sender:
                queryset = queryset.filter(sender_event__sender=sender)
            elif public:
                queryset = queryset.filter(sender_event__sender__isnull=True)
            self.fields['files'].queryset = queryset
