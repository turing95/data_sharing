from allauth.socialaccount.views import ConnectionsView as AllAuthConnectionsView
from django.urls import reverse_lazy


class ConnectionsView(AllAuthConnectionsView):
    success_url = reverse_lazy("account_settings")
