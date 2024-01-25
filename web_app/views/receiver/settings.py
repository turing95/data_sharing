from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from web_app.mixins import SubscriptionMixin
from web_app.forms import CustomSocialDisconnectForm


class SettingsView(LoginRequiredMixin, SubscriptionMixin, TemplateView):
    template_name = "private/settings/settings.html"

    def get_form_kwargs(self):
        kwargs = {'request': self.request}
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['disconnect_form'] = CustomSocialDisconnectForm(**self.get_form_kwargs())
        context['settings_page'] = True        
        context['google_account_connected'] = self.request.custom_user.google_account is not None
        context['microsoft_account_connected'] = self.request.custom_user.microsoft_account is not None
        return context
