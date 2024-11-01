from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import TemplateView
from web_app.mixins import SubscriptionMixin, GrantSideBarMixin, GrantMixin, GrantTabMixin


class GrantDetailView(LoginRequiredMixin, SubscriptionMixin, GrantSideBarMixin, GrantTabMixin, GrantMixin,
                      TemplateView):
    template_name = 'private/grant/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['grant_tab']['detail']['active'] = True
        return context


class GrantChecklistView(LoginRequiredMixin, SubscriptionMixin, GrantSideBarMixin, GrantTabMixin, GrantMixin,
                         TemplateView):
    template_name = 'private/grant/checklist.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['grant_tab']['checklist']['active'] = True
        return context
