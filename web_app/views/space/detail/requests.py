from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from web_app.mixins import SubscriptionMixin, SpaceMixin, SpaceSideBarMixin, SpaceTabMixin


class SpaceRequestsView(LoginRequiredMixin, SubscriptionMixin, SpaceMixin, SpaceSideBarMixin, SpaceTabMixin,
                        ListView):
    template_name = "private/space/detail/request/list.html"
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['space_summary'] = True
        context['space_tab']['requests']['active'] = True
        return context
    
    def get_queryset(self):
        return self.get_space().requests.all().order_by('created_at')
