from django import forms
from web_app.forms.css_classes.inputs import text_input
from django.utils.translation import gettext_lazy as _

from web_app.models import Organization


class OrganizationCreateForm(forms.ModelForm):
    name = forms.CharField(label=_("Name"),
                           widget=forms.TextInput(attrs={'placeholder': _('Name'), 'class': text_input}))

    class Meta:
        model = Organization
        fields = ('name',)


class OrganizationForm(forms.ModelForm):
    name = forms.CharField(label=_("Organization name"),
                           widget=forms.TextInput(attrs={'placeholder': _('Name'), 'class': text_input}),
                           help_text=_("Organization name"))

    class Meta:
        model = Organization
        fields = ('name',)