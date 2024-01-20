from django.views.generic import TemplateView
from web_app.mixins import SubscriptionMixin


class PublicLandingView(SubscriptionMixin,TemplateView):
    template_name = 'public/public_landing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['generic_home'] = True
        return context

