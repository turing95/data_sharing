from django.views.generic import ListView
from web_app.models import Space
from django.contrib.auth.mixins import LoginRequiredMixin


class SpacesView(LoginRequiredMixin, ListView):
    model = Space
    template_name = "receiver/private/spaces.html"
    paginate_by = 5

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
