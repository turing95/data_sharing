from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from web_app.mixins import SubscriptionMixin, SpaceMixin, SpaceSideBarMixin, SpaceTabMixin


class SpaceRequestsView(LoginRequiredMixin, SubscriptionMixin, SpaceMixin, SpaceSideBarMixin, SpaceTabMixin,
                        TemplateView):
    template_name = "private/space/detail/request/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['space_summary'] = True
        context['space_tab']['requests']['active'] = True
        return context
