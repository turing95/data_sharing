from django.views.generic import TemplateView
from web_app.views.unrestricted_page import UnrestrictedAccessMixin

class PublicLandingView(UnrestrictedAccessMixin, TemplateView):
    template_name = 'public/public_landing.html'
