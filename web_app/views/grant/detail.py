from django.views.generic import TemplateView
from web_app.mixins import SubscriptionMixin, GrantSideBarMixin, GrantMixin


class GrantDetailView(SubscriptionMixin, GrantSideBarMixin,GrantMixin, TemplateView):
    template_name = "private/grant/detail.html"
