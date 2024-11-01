from django.views.generic import TemplateView
from web_app.mixins import SenderTabMixin, SpaceSenderMixin


class SpaceDetailView(SenderTabMixin, SpaceSenderMixin, TemplateView):
    template_name = "sender/base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sender_tab']['detail']['active'] = True
        return context
