from django import forms
from web_app.forms.css_classes.inputs import text_input

from web_app.models import Company


class CompanyForm(forms.ModelForm):
    name = forms.CharField(label="Name",
                           widget=forms.TextInput(attrs={'placeholder': 'Name', 'class': text_input}))

    class Meta:
        model = Company
        fields = ('name',)
