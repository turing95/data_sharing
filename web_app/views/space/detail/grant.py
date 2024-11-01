from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import FormView, TemplateView
from web_app.mixins import SubscriptionMixin, SpaceMixin, SpaceSideBarMixin, SpaceTabMixin
from web_app.models import Grant


class SpaceGrantView(LoginRequiredMixin, SubscriptionMixin, SpaceMixin, SpaceSideBarMixin, SpaceTabMixin, TemplateView):
    template_name = "private/space/detail/base.html"
    _grant = None

    def get_grant(self):
        if not self._grant:
            self._grant = get_object_or_404(Grant, pk=self.kwargs['grant_uuid'])
        return self._grant

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grant'] = self.get_grant()
        context['space_tab']['grant']['active'] = True
        return context