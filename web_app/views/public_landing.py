from django.views.generic import TemplateView


class PublicLandingView(TemplateView):
    template_name = 'public/public_landing.html'
