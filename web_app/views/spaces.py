from django.views.generic import TemplateView
from web_app.models import Space


class SpacesView(TemplateView):
    template_name = "spaces.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["spaces"] = Space.objects.all()
        return context
