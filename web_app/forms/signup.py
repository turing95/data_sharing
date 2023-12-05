from allauth.account import app_settings
from allauth.account.forms import SignupForm as AllauthSignupForm
from django import forms
from web_app.forms import css_classes


class SignupForm(AllauthSignupForm):
    username = forms.CharField(
        label="Username",
        min_length=app_settings.USERNAME_MIN_LENGTH,
        widget=forms.TextInput(
            attrs={"placeholder": "Username", "autocomplete": "username", "class": css_classes.text_input}
        ),
    )
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "type": "email",
                "placeholder": "Email address",
                "autocomplete": "email",
                "class": css_classes.text_input
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs["class"] = css_classes.text_input
        if app_settings.SIGNUP_PASSWORD_ENTER_TWICE:
            self.fields["password2"].widget.attrs["class"] = css_classes.text_input