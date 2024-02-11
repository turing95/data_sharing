from web_app.forms import css_classes
from web_app.forms.css_classes import text_input ,language_input
from web_app.models import SenderNotificationsSettings
from django import forms


class SenderNotificationsSettingsForm(forms.ModelForm):
    name = forms.CharField(required=False, label="Name",
                           widget=forms.TextInput(attrs={'placeholder': 'Name', 'class': text_input}),
                           help_text="This name will be used as the reference name displayed in all notifications sent to the senders.")
    reference_email = forms.CharField(required=False, label="Reference Email",
                                      widget=forms.TextInput(
                                          attrs={'placeholder': 'Reference Email', 'class': text_input}),
                                      help_text="This email will be used as the reference email displayed in all notifications sent to the senders.")
    language = forms.ChoiceField(required=False, label="Language",
                                 widget=forms.Select(attrs={'class': language_input}),
                                 help_text="This language will be used as the preferred language for all notifications sent to the senders.",
                                 choices=[('en', 'English'), ('it', 'Italiano')])

    class Meta:
        model = SenderNotificationsSettings
        fields = ('name', 'reference_email', 'language')
