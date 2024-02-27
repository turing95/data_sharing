from django.shortcuts import redirect
from django.views.generic import ListView
from web_app.models import Space, Organization
from django.contrib.auth.mixins import LoginRequiredMixin
from web_app.mixins import SubscriptionMixin, OrganizationMixin, SideBarMixin


class SpacesView(LoginRequiredMixin, SubscriptionMixin, OrganizationMixin,SideBarMixin, ListView):
    model = Space
    template_name = "private/space/list.html"
    paginate_by = 12

    def dispatch(self, request, *args, **kwargs):
        if not kwargs.get('organization_uuid'):
            return redirect('spaces', organization_uuid=self.request.user.organizations.first().pk)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

    def get_queryset(self):
        return self.model.objects.filter(organization=self.kwargs.get('organization_uuid'),
                                         organization__in=self.request.user.organizations.all(),
                                         is_deleted=False)
