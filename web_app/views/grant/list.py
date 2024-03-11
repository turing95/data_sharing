from django.views.generic import ListView
from web_app.mixins import OrganizationMixin, GrantSideBarMixin, SubscriptionMixin


class GrantListView(OrganizationMixin, GrantSideBarMixin, SubscriptionMixin, ListView):
    template_name = "private/grant/list.html"
    paginate_by = 12

    def get_queryset(self):
        return self.get_organization().grants.all().order_by('created_at')
