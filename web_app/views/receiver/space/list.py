from django.views.generic import ListView
from web_app.models import Space
from django.contrib.auth.mixins import LoginRequiredMixin
from web_app.mixins import SubscriptionMixin
from django.conf import settings

class SpacesView(LoginRequiredMixin,SubscriptionMixin, ListView):
    model = Space
    template_name = "private/space/list.html"
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new_space_button_text'] = 'NEW SPACE' if context['user_maxed_spaces'] is False else 'UPGRADE TO CREATE MORE SPACES'
        return context
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user, is_deleted=False)
