from allauth.socialaccount.views import ConnectionsView as AllAuthConnectionsView
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy


class ConnectionsView(AllAuthConnectionsView):
    success_url = reverse_lazy("account_settings")

    def get(self, request, *args, **kwargs):
        raise Http404()
