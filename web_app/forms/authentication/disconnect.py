from allauth.socialaccount.forms import DisconnectForm
from django import forms


class CustomSocialDisconnectForm(DisconnectForm):
    account_to_disconnect = forms.CharField(widget=forms.HiddenInput(
                                             attrs={'class': 'account-to-disconnect-input'}))
    
    def __init__(self, *args, **kwargs):
        super(CustomSocialDisconnectForm, self).__init__(*args, **kwargs)
        self.fields['account'].required = False
        
    
    def clean(self):
        # Access the form data and modify the "account" field as needed
        account_to_disconnect= self.cleaned_data.get("account_to_disconnect")
        account = self.accounts.filter(provider=account_to_disconnect).first()
        self.cleaned_data["account"] = account

        # Now call the superclass's clean method to continue with the original logic
        cleaned_data = super(CustomSocialDisconnectForm, self).clean()

        return cleaned_data
    
    def save(self):
        # Add your own processing here if you do need access to the
        # socialaccount being deleted.

        # Ensure you call the parent class's save.
        # .save() does not return anything
        super(CustomSocialDisconnectForm, self).save()

        # Add your own processing here if you don't need access to the
        # socialaccount being deleted.