from django import forms
from web_app.forms.css_classes.inputs import text_input, text_input_label

from web_app.models import User


class UserForm(forms.ModelForm):
    first_name = forms.CharField(required=False, label="First name",
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': text_input}))
    last_name = forms.CharField(required=False, label="Last name",
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': text_input}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name')
