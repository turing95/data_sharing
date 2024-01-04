from django.views.generic import TemplateView
from web_app.views.unrestricted_page import UnrestrictedAccessMixin

class PrivacyPolicyView(UnrestrictedAccessMixin,TemplateView):
    template_name = 'public/privacy_policy.html'
