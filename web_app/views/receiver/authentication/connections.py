from allauth.socialaccount.views import ConnectionsView as AllAuthConnectionsView
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from web_app.forms import CustomSocialDisconnectForm


class ConnectionsView(AllAuthConnectionsView):
    success_url = reverse_lazy("account_settings")
    form_class = CustomSocialDisconnectForm

    def get(self, request, *args, **kwargs):
        raise Http404()

    def form_invalid(self, form):
        print(form.errors)
        return redirect(self.success_url)
