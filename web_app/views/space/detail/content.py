from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView
from web_app.forms import SpaceContentForm
from web_app.mixins import SubscriptionMixin, SpaceMixin, SpaceSideBarMixin, SpaceTabMixin


class SpaceContentView(LoginRequiredMixin, SubscriptionMixin, SpaceMixin, SpaceSideBarMixin, SpaceTabMixin, FormView):
    template_name = "private/space/detail/content.html"
    form_class = SpaceContentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['space_tab']['content']['active'] = True
        return context
