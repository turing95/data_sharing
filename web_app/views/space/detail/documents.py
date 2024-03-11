from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, TemplateView
from web_app.mixins import SubscriptionMixin, SpaceMixin, SpaceSideBarMixin, SpaceTabMixin


class SpaceDocumentsView(LoginRequiredMixin, SubscriptionMixin, SpaceMixin, SpaceSideBarMixin, SpaceTabMixin,
                         TemplateView):
    template_name = "private/space/detail/documents.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['space_tab']['documents']['active'] = True
        return context
