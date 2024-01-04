from allauth.account.views import SignupView as AllauthSignupView
from web_app.forms.signup import SignupForm
from django.urls import reverse_lazy
from web_app.views.receiver.authentication.auth_page import AuthPageMixin


class SignupView(AuthPageMixin,AllauthSignupView):
    form_class = SignupForm
    template_name = 'public/authentication/signup.html'
    success_url = reverse_lazy('spaces')
