from web_app.forms import css_classes
from web_app.forms.css_classes import text_input, language_input
from web_app.models import SenderNotificationsSettings, NotificationsSettings
from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _


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
                                 choices=[(lang[0], _(lang[1].capitalize())) for lang in settings.LANGUAGES])

    class Meta:
        model = SenderNotificationsSettings
        fields = ('name', 'reference_email', 'language')


class NotificationsSettingsForm(forms.ModelForm):
    on_sender_upload = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': css_classes.checkbox_input}),
        required=False,
        label='Upload notification',
        help_text="""Receive a notification when a sender uploads a file to your space. This notification will be sent to the email address you have registered with us.""")

    class Meta:
        model = NotificationsSettings
        fields = ('on_sender_upload',)
