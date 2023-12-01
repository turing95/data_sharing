from allauth.account.forms import LoginForm as AllauthLoginForm
from django.urls import reverse
from django.utils.safestring import mark_safe

from web_app.forms.css_classes import text_input
 

class LoginForm(AllauthLoginForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        reset_url = reverse("account_reset_password")
        self.fields["password"].widget.attrs["class"] = text_input
        self.fields["password"].help_text = mark_safe(
            f'<p class="text-sm">Forgot your password? <a href="{reset_url}" class="text-blue-600 hover:text-blue-600 underline">Reset</a></p>'
        )

        self.fields["login"].widget.attrs["class"] = text_input
