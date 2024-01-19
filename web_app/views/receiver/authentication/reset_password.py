from allauth.account.views import PasswordResetView as AllauthPasswordResetView
from web_app.forms.authentication.reset_password import ResetPasswordForm


class PasswordResetView(AllauthPasswordResetView):
    template_name = 'public/authentication/reset_password.html'
    form_class = ResetPasswordForm
