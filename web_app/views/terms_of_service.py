from django.views.generic import TemplateView


class TermsOfServiceView(TemplateView):
    template_name = 'public/terms_of_service.html'
