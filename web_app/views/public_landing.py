from django.views.generic import TemplateView
from web_app.mixins import SubscriptionMixin


class PublicLandingView(SubscriptionMixin,TemplateView):
    template_name = 'public/public_landing.html'
