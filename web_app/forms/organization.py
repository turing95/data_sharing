from django import forms
from web_app.forms.css_classes.inputs import text_input
from django.utils.translation import gettext_lazy as _

from web_app.models import Organization


class OrganizationForm(forms.ModelForm):
    name = forms.CharField(label=_("Name"),
                           widget=forms.TextInput(attrs={'placeholder': _('Name'), 'class': text_input}))

    class Meta:
        model = Organization
        fields = ('name',)
