from django.views.generic import TemplateView
from web_app.mixins import SubscriptionMixin


class PrivacyPolicyView(SubscriptionMixin,TemplateView):
    template_name = 'public/privacy_policy.html'
