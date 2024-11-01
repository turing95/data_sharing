from django import forms
from web_app.forms.css_classes.inputs import text_input, text_input_label
from django.utils.translation import gettext_lazy as _

from web_app.models import User


class UserForm(forms.ModelForm):
    first_name = forms.CharField(required=False, label=_("First name"),
                                 widget=forms.TextInput(attrs={'placeholder': _('First Name'), 'class': text_input}))
    last_name = forms.CharField(required=False, label=_("Last name"),
                                widget=forms.TextInput(attrs={'placeholder': _('Last Name'), 'class': text_input}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name')
