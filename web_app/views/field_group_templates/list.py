from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from web_app.mixins import OrganizationMixin, CompanySideBarMixin, SubscriptionMixin
from web_app.models import Organization, FieldGroup


class FieldGroupTemplatesListView(OrganizationMixin, CompanySideBarMixin, SubscriptionMixin, ListView):
    template_name = "private/company_templates/list.html"
    paginate_by = 12

    def get_queryset(self):
        return self.get_organization().field_group_templates.all().order_by('-created_at')


@require_POST
@login_required
def search_templates(request, group_uuid):
    templates = []
    group = get_object_or_404(FieldGroup, pk=group_uuid)
    search_query = request.POST.get('search-templates')
    if search_query:
        templates = group.organization.field_group_templates.filter(
            group__label__icontains=search_query
        )
    return render(request,
                  'private/company_templates/search/results.html',
                  {'templates': templates, 'search_query': search_query, 'group': group})
