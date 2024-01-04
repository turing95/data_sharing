from allauth.account.views import LoginView as AllauthLoginView
from django.urls import reverse_lazy
from web_app.forms.login import LoginForm
from web_app.views.receiver.authentication.auth_page import AuthPageMixin


class LoginView(AuthPageMixin,AllauthLoginView):
    form_class = LoginForm
    success_url = reverse_lazy('spaces')
    template_name = 'public/authentication/login.html'
