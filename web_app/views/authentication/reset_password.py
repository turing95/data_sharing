from allauth.account.views import (PasswordResetView as AllauthPasswordResetView,
                                   PasswordResetFromKeyView as AllauthPasswordResetFromKeyView,
                                   PasswordResetDoneView as AllauthPasswordResetDoneView,
                                   PasswordResetFromKeyDoneView as AllauthPasswordResetFromKeyDoneView)

from web_app.forms.authentication.reset_password import ResetPasswordForm


class PasswordResetView(AllauthPasswordResetView):
    template_name = 'authentication/reset_password.html'
    form_class = ResetPasswordForm


class PasswordResetDoneView(AllauthPasswordResetDoneView):
    template_name = 'authentication/password_reset_done.html'


class PasswordResetFromKeyView(AllauthPasswordResetFromKeyView):
    template_name = 'authentication/password_reset_from_key.html'


class PasswordResetFromKeyDoneView(AllauthPasswordResetFromKeyDoneView):
    template_name = 'authentication/password_reset_from_key_done.html'
