from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from web_app.mixins import SubscriptionMixin, SpaceMixin, SpaceSideBarMixin
from web_app.mixins import SpaceTabMixin


class HistoryListView(LoginRequiredMixin, SubscriptionMixin, SpaceMixin, SpaceSideBarMixin, SpaceTabMixin,
                      TemplateView):
    template_name = 'private/space/detail/event/history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['space_tab']['history']['active'] = True
        return context
