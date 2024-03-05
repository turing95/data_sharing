from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from web_app.models import Sender
from web_app.mixins import SubscriptionMixin, SpaceMixin, SpaceSideBarMixin


class SenderListView(LoginRequiredMixin, SubscriptionMixin, SpaceMixin, SpaceSideBarMixin, ListView):
    template_name = 'private/space/detail/sender/list.html'
    model = Sender
    paginate_by = 10

    def get_queryset(self):
        return self.get_space().senders.all()
