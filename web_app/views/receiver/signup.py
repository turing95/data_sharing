from allauth.account.views import SignupView as AllauthSignupView
from web_app.forms.signup import SignupForm
from django.urls import reverse_lazy


class SignupView(AllauthSignupView):
    form_class = SignupForm
    template_name = 'receiver/public/signup.html'
    success_url = reverse_lazy('spaces')
