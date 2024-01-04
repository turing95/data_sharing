from allauth.account.views import PasswordResetView as AllauthPasswordResetView
from web_app.forms.reset_password import ResetPasswordForm
from web_app.views.receiver.authentication.auth_page import AuthPageMixin


class PasswordResetView(AuthPageMixin,AllauthPasswordResetView):
    template_name = 'public/authentication/reset_password.html'
    form_class = ResetPasswordForm
