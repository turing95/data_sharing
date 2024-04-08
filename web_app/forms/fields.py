from django import forms
from django.urls import reverse_lazy

from web_app.forms import css_classes
from django.utils.translation import gettext_lazy as _
from web_app.models import TextField, FieldGroup
from django.core.exceptions import ValidationError


class TextFieldSetForm(forms.ModelForm):
    label = forms.CharField(widget=forms.TextInput(attrs={'class': css_classes.text_input,
                                                          }))
    multiple = forms.BooleanField(required=False,
                                  widget=forms.CheckboxInput(attrs={'class': css_classes.checkbox_input,
                                                                    }),
                                  label=_('Multiple values'))

    class Meta:
        model = TextField
        fields = ['label', 'multiple']

    def __init__(self, *args, **kwargs):
        self.group = kwargs.pop('group')
        super().__init__(*args, **kwargs)

    def clean_label(self):
        label = self.cleaned_data['label']

        if self.group.fields.filter(label=label).exclude(pk=self.instance.pk).exists():
            raise ValidationError(_("A field with this label already exists in this group."))

        return label


class FieldGroupSetForm(forms.ModelForm):
    label = forms.CharField(widget=forms.TextInput(attrs={'class': css_classes.text_input,
                                                          }))
    multiple = forms.BooleanField(required=False,
                                  widget=forms.CheckboxInput(attrs={'class': css_classes.checkbox_input,
                                                                    }),
                                  label=_('Multiple values'))

    class Meta:
        model = FieldGroup
        fields = ['label', 'multiple']

    def __init__(self, *args, **kwargs):
        self.group = kwargs.pop('group')
        super().__init__(*args, **kwargs)

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance is not None:
            self.fields['value'].widget.attrs['hx-post'] = reverse_lazy('text_field_update_value',
                                                                        kwargs={'field_uuid': self.instance.pk})

    class Meta:
        model = TextField
        fields = ['value']
