from allauth.account.views import PasswordResetView as AllauthPasswordResetView


class PasswordResetView(AllauthPasswordResetView):
    template_name = 'receiver/public/password_reset.html'
