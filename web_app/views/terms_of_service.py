from django.views.generic import TemplateView
from web_app.views.unrestricted_page import UnrestrictedAccessMixin

class TermsOfServiceView(UnrestrictedAccessMixin, TemplateView):
    template_name = 'public/terms_of_service.html'
