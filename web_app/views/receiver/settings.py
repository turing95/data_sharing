from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = "private/settings.html"

