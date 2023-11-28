from allauth.account.views import PasswordResetView as AllauthPasswordResetView
from django.urls import reverse_lazy
from web_app.forms.login import LoginForm


class LoginView(AllauthPasswordResetView):
    form_class = LoginForm
    success_url = reverse_lazy('spaces')
    template_name = 'receiver/public/login.html'