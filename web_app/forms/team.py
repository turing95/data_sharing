from django import forms
from web_app.forms.css_classes.inputs import text_input
from django.utils.translation import gettext_lazy as _


from web_app.models import Organization


class TeamInviteForm(forms.Form):
    email = forms.EmailField(label=_("Invite collaborator:"),
                             widget=forms.EmailInput(attrs={'placeholder': _('user@mail.com'), 'class': text_input}))

    def __init__(self, *args, **kwargs):
        self.organization = kwargs.pop('organization', None)
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']
        if self.organization.users.filter(email=email).exists():
            raise forms.ValidationError(_('User already in organization'))
        if self.organization.invitations.filter(email=email).exists():
            raise forms.ValidationError(_('User already invited'))
        return email
