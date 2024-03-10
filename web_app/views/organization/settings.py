from django.views.generic import FormView
from web_app.mixins import OrganizationMixin, SubscriptionMixin, SideBarMixin
from django.utils.translation import gettext_lazy as _


class OrganizationSettingsSideBarMixin(SideBarMixin):
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['sidebar']['settings'] = True
        return data


class OrganizationSettingsView(SubscriptionMixin, OrganizationMixin, OrganizationSettingsSideBarMixin, FormView):
    template_name = "private/organization/settings.html"