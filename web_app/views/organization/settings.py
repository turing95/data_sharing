from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from web_app.forms import SenderNotificationsSettingsForm
from web_app.mixins import OrganizationMixin, SubscriptionMixin, OrganizationSettingsSideBarMixin
from web_app.models import SenderNotificationsSettings


class OrganizationSettingsView(LoginRequiredMixin, OrganizationMixin, OrganizationSettingsSideBarMixin, SubscriptionMixin, TemplateView):
    template_name = "private/organization/settings.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        try:
            context['sender_notifications_form'] = SenderNotificationsSettingsForm(
                instance=self.get_organization().sender_notifications_settings)
        except SenderNotificationsSettings.DoesNotExist:
            SenderNotificationsSettings.objects.create(organization=self.get_organization())
            context['sender_notifications_form'] = SenderNotificationsSettingsForm(
                instance=self.get_organization().sender_notifications_settings)
        context['organization_can_delete'] = self.get_organization().can_delete(self.request.user)
        return context
