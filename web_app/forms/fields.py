from django import forms
from django.urls import reverse_lazy

from web_app.forms import css_classes
from django.utils.translation import gettext_lazy as _

from web_app.forms.widgets import MultipleFileField
from web_app.models import TextField, FieldGroup, FileField
from django.core.exceptions import ValidationError


class BaseFieldSetForm(forms.ModelForm):
    label = forms.CharField(widget=forms.TextInput(attrs={'class': css_classes.text_input,
                                                          }))
    multiple = forms.BooleanField(required=False,
                                  widget=forms.CheckboxInput(attrs={'class': css_classes.checkbox_input,
                                                                    }),
                                  label=_('Multiple values'))

    def __init__(self, *args, **kwargs):
        self.group = kwargs.pop('group')
        super().__init__(*args, **kwargs)


class TextFieldSetForm(BaseFieldSetForm):
    class Meta:
        model = TextField
        fields = ['label', 'multiple']

    def clean_label(self):
        label = self.cleaned_data['label']

        if self.group.text_fields.filter(label=label).exclude(pk=self.instance.pk).exists():
            raise ValidationError(_("A field with this label already exists in this group."))

        return label


class FileFieldSetForm(BaseFieldSetForm):
    multiple_files = forms.BooleanField(required=False,
                                        widget=forms.CheckboxInput(attrs={'class': css_classes.checkbox_input,
                                                                          }),
                                        label=_('Multiple files'))

    class Meta:
        model = FileField
        fields = ['label', 'multiple', 'multiple_files']

    def clean_label(self):
        label = self.cleaned_data['label']

        if self.group.file_fields.filter(label=label).exclude(pk=self.instance.pk).exists():
            raise ValidationError(_("A field with this label already exists in this group."))

        return label


class FieldGroupSetForm(BaseFieldSetForm):
    class Meta:
        model = FieldGroup
        fields = ['label', 'multiple']

    def clean_label(self):
        label = self.cleaned_data['label']

        if self.group is not None and self.group.groups.filter(label=label).exclude(pk=self.instance.pk).exists():
            raise ValidationError(_("A group with this label already exists in this group."))

        return label


class TextFieldFillForm(forms.ModelForm):
    value = forms.CharField(required=False,
                            widget=forms.TextInput(attrs={'class': css_classes.text_input,
                                                          'hx-trigger': 'blur changed',
                                                          'hx-target': 'closest .field-container',
                                                          'hx-swap': 'outerHTML'

                                                          }),
                            )

    class Meta:
        model = TextField
        fields = ['value']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance is not None:
            self.fields['value'].widget.attrs['hx-post'] = reverse_lazy('text_field_update_value',
                                                                        kwargs={'field_uuid': self.instance.pk})


class FileFieldFillForm(forms.ModelForm):

    class Meta:
        model = FileField
        fields = []



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance is not None:
            self.fields['files'] = MultipleFileField(multiple_files=self.instance.multiple_files, label='Files',
                                                     required=False)
            self.fields['files'].widget.attrs['hx-post'] = reverse_lazy('file_field_update_value',
                                                                       kwargs={'field_uuid': self.instance.pk})
            self.fields['files'].widget.attrs['hx-swap'] = 'none'
            self.fields['files'].widget.attrs['hx-trigger'] = 'change'

