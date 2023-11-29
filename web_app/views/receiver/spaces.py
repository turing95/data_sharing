# from django.views.generic import TemplateView 
# from web_app.models import Space
# from django.contrib.auth.mixins import LoginRequiredMixin


# class SpacesView(LoginRequiredMixin,TemplateView):
#     template_name = "receiver/private/spaces.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["spaces"] = Space.objects.filter(user=self.request.user)
#         return context

from django.views.generic import ListView
from web_app.models import Space
from django.contrib.auth.mixins import LoginRequiredMixin

class SpacesView(LoginRequiredMixin, ListView):
    model = Space
    template_name = "receiver/private/spaces.html"
    paginate_by = 5  # Adjust the number of items per page as needed

    def get_queryset(self):
        # Return spaces filtered by the logged-in user
        return Space.objects.filter(user=self.request.user)
