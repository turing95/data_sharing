from allauth.account.views import LoginView as AllauthLoginView
from allauth.socialaccount.views import LoginCancelledView as AllauthLoginCancelledView
from django.urls import reverse_lazy
from web_app.forms.authentication.login import LoginForm


class LoginView(AllauthLoginView):
    form_class = LoginForm
    success_url = reverse_lazy('spaces')
    template_name = 'authentication/login.html'


class LoginCancelledView(AllauthLoginCancelledView):
    template_name = 'authentication/login_cancelled.html'
