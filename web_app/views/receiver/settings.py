from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from web_app.mixins import SubscriptionMixin


class SettingsView(LoginRequiredMixin,SubscriptionMixin, TemplateView):
    template_name = "private/settings.html"

