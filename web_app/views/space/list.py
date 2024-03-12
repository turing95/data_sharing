from django.shortcuts import redirect
from django.views.generic import ListView
from web_app.models import Space
from django.contrib.auth.mixins import AccessMixin
from web_app.mixins import SubscriptionMixin, OrganizationMixin, SideBarMixin


class SpaceSideBarMixin(SideBarMixin):
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['sidebar']['space'] = True
        return data


class SpacesView(AccessMixin, SubscriptionMixin, OrganizationMixin, SpaceSideBarMixin, ListView):
    model = Space
    template_name = "private/space/list/list.html"
    paginate_by = 12

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
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
