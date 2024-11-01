from django.views.generic import TemplateView
from web_app.mixins import SenderTabMixin, SpaceSenderMixin


class RequestListView(SenderTabMixin, SpaceSenderMixin, TemplateView):
    template_name = "sender/request/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sender_tab']['requests']['active'] = True
        return context
