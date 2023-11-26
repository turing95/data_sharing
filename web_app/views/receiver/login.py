from allauth.account.views import LoginView as AllauthLoginView
from django.urls import reverse_lazy


class LoginView(AllauthLoginView):
    success_url = reverse_lazy('spaces')
