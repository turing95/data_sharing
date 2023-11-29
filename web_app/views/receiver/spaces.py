from django.views.generic import TemplateView 
from web_app.models import Space
from django.contrib.auth.mixins import LoginRequiredMixin


class SpacesView(LoginRequiredMixin,TemplateView):
    template_name = "receiver/private/spaces.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["spaces"] = Space.objects.filter(user=self.request.user)
        return context
