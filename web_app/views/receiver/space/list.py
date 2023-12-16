from django.views.generic import ListView
from web_app.models import Space
from django.contrib.auth.mixins import LoginRequiredMixin


class SpacesView(LoginRequiredMixin, ListView):
    model = Space
    template_name = "private/space/list.html"
    paginate_by = 12

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
