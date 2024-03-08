from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from web_app.models import Sender
from web_app.mixins import SubscriptionMixin, SpaceMixin, SpaceSideBarMixin
from web_app.views.space.detail import SpaceTabMixin


class SenderListView(LoginRequiredMixin, SubscriptionMixin, SpaceMixin, SpaceSideBarMixin, SpaceTabMixin,  ListView):
    template_name = 'private/space/detail/sender/list.html'
    model = Sender
    paginate_by = 10
    
    #set context space_tab to active
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['space_tab']['share']['active'] = True
        return context

    def get_queryset(self):
        return self.get_space().senders.all()
