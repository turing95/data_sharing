from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView
from web_app.mixins import SubscriptionMixin


class PublicLandingView(SubscriptionMixin, TemplateView):
    template_name = 'public/public_landing.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('spaces'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['generic_home'] = True
        return context
