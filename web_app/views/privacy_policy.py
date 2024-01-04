from django.views.generic import TemplateView


class PrivacyPolicyView(TemplateView):
    template_name = 'public/privacy_policy.html'
