from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from web_app.mixins import SubscriptionMixin
from web_app.forms import CustomSocialDisconnectForm, UserForm, SenderNotificationsSettingsForm
from web_app.models import SenderNotificationsSettings


class SettingsView(LoginRequiredMixin, SubscriptionMixin, TemplateView):
    template_name = "private/settings/settings.html"

    def get_form_kwargs(self):
        kwargs = {'request': self.request}
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['user_form'] = UserForm(instance=self.request.user)
        print(repr(self.request.user.email))
        try:
            context['sender_notifications_form'] = SenderNotificationsSettingsForm(instance=self.request.user.sender_notifications_settings)
        except SenderNotificationsSettings.DoesNotExist:
            SenderNotificationsSettings.objects.create(user=self.request.user)
            context['sender_notifications_form'] = SenderNotificationsSettingsForm(instance=self.request.user.sender_notifications_settings)
        context['disconnect_form'] = CustomSocialDisconnectForm(**self.get_form_kwargs())
        context['settings_page'] = True
        return context
