from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from web_app.mixins import SubscriptionMixin
from web_app.forms import CustomSocialDisconnectForm, UserForm, SenderNotificationsSettingsForm, \
    NotificationsSettingsForm
from web_app.models import SenderNotificationsSettings, NotificationsSettings


class SettingsView(LoginRequiredMixin, SubscriptionMixin, TemplateView):
    template_name = "private/settings/settings.html"

    def get_form_kwargs(self):
        kwargs = {'request': self.request}
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['user_form'] = UserForm(instance=self.request.user)
        try:
            context['sender_notifications_form'] = SenderNotificationsSettingsForm(instance=self.request.user.sender_notifications_settings)
        except SenderNotificationsSettings.DoesNotExist:
            SenderNotificationsSettings.objects.create(user=self.request.user)
            context['sender_notifications_form'] = SenderNotificationsSettingsForm(instance=self.request.user.sender_notifications_settings)
        try:
            context['notifications_form'] = NotificationsSettingsForm(instance=self.request.user.notifications_settings)
        except SenderNotificationsSettings.DoesNotExist:
            NotificationsSettings.objects.create(user=self.request.user)
            context['notifications_form'] = NotificationsSettingsForm(instance=self.request.user.notifications_settings)
        context['disconnect_form'] = CustomSocialDisconnectForm(**self.get_form_kwargs())
        context['settings_page'] = True
        return context
