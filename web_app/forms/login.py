from allauth.account.forms import LoginForm as AllauthLoginForm
from web_app.forms.css_classes import text_input


class LoginForm(AllauthLoginForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].widget.attrs["class"] = text_input
        self.fields["login"].widget.attrs["class"] = text_input
