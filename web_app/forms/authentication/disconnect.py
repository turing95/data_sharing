from allauth.socialaccount.forms import DisconnectForm
from django import forms

from web_app.models import UploadRequest


class CustomSocialDisconnectForm(DisconnectForm):
    account_to_disconnect = forms.CharField(widget=forms.HiddenInput(
        attrs={'class': 'account-to-disconnect-input'}))

    def __init__(self, *args, **kwargs):
        super(CustomSocialDisconnectForm, self).__init__(*args, **kwargs)
        self.fields['account'].required = False

    def clean(self):
        # Access the form data and modify the "account" field as needed
        account_to_disconnect = self.cleaned_data.get("account_to_disconnect")
        account = self.accounts.filter(provider=account_to_disconnect).first()
        self.cleaned_data["account"] = account

        # Now call the superclass's clean method to continue with the original logic
        cleaned_data = super(CustomSocialDisconnectForm, self).clean()

        return cleaned_data

    def save(self):
        account = self.cleaned_data['account']
        UploadRequest.objects.filter(destinations__social_account=account).update(is_deleted=True)
        super(CustomSocialDisconnectForm, self).save()
