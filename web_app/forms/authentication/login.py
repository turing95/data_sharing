from allauth.account.forms import LoginForm as AllauthLoginForm
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.utils.text import format_lazy

from web_app.forms.css_classes import text_input


class LoginForm(AllauthLoginForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        reset_url = reverse("account_reset_password")
        self.fields["password"].widget.attrs["class"] = text_input
        help_text_copy = _("Forgot your password?")
        help_text_copy_2 = _("Reset")
        self.fields["password"].help_text = mark_safe(
            format_lazy('<p class="text-sm">{help_text_copy} <a href="{reset_url}" class="text-blue-600 underline hover:text-blue-600">{help_text_copy_2}</a></p>', help_text_copy=help_text_copy, reset_url=reset_url, help_text_copy_2=help_text_copy_2)
        )

        self.fields["login"].widget.attrs["class"] = text_input
