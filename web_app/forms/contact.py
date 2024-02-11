from django import forms
from web_app.forms.css_classes.inputs import text_input

from web_app.models import Contact


class ContactForm(forms.ModelForm):
    first_name = forms.CharField(required=False, label="First name",
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': text_input}))
    last_name = forms.CharField(required=False, label="Last name",
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': text_input}))
    email = forms.CharField(label="Email",
                                widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': text_input}))

    class Meta:
        model = Contact
        fields = ('first_name', 'last_name','email')
