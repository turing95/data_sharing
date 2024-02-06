from web_app.forms.css_classes import text_input
from web_app.models import SenderNotificationsSettings
from django import forms


class SenderNotificationsSettingsForm(forms.ModelForm):
    name = forms.CharField(required=False, label="Name",
                           widget=forms.TextInput(attrs={'placeholder': 'Name', 'class': text_input}))
    reference_email = forms.CharField(required=False, label="Reference Email",
                                      widget=forms.TextInput(attrs={'placeholder': 'Reference Email', 'class': text_input}))

    class Meta:
        model = SenderNotificationsSettings
        fields = ('name', 'reference_email')
