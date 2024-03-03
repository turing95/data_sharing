from django import forms
from web_app.forms.css_classes.inputs import text_input
from django.utils.translation import gettext_lazy as _

from web_app.models import Company


class CompanyForm(forms.ModelForm):
    name = forms.CharField(label=_("Name"),
                           widget=forms.TextInput(attrs={'placeholder': _('Name'), 'class': text_input}))

    class Meta:
        model = Company
        fields = ('name',)
