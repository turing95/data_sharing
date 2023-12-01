from django.views.generic import TemplateView

class PrivacyPolicyView(TemplateView):
    template_name = 'receiver/public/privacy_policy.html'
