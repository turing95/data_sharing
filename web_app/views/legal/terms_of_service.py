from django.views.generic import TemplateView
from web_app.mixins import SubscriptionMixin


class TermsOfServiceView(SubscriptionMixin,TemplateView):
    template_name = 'public/terms_of_service.html'
