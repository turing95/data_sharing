from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _

from web_app.mixins import SpaceSideBarMixin, RequestMixin, SubscriptionMixin, RequestTabMixin


class RequestDetailView(LoginRequiredMixin, SubscriptionMixin, RequestMixin, SpaceSideBarMixin, RequestTabMixin,
                        TemplateView):
    template_name = 'private/request/base.html'
 
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['request_tab']['detail']['active'] = True
        context['inputs_tooltip_content'] =_("Check what have been submitted for your inputs below")
        return context
