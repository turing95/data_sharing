from allauth.account.views import LoginView as AllauthLoginView
from django.urls import reverse_lazy
from web_app.forms.login import LoginForm


class LoginView(AllauthLoginView):
    form_class = LoginForm
    success_url = reverse_lazy('spaces')
    template_name = 'receiver/public/login.html'
