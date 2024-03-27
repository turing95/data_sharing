from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseBadRequest
from django.views.generic import ListView
from web_app.mixins import OrganizationMixin, CompanySideBarMixin, SubscriptionMixin
from web_app.models import Organization

class CompanyListView(OrganizationMixin, CompanySideBarMixin, SubscriptionMixin, ListView):
    template_name = "private/company/list.html"
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return self.get_organization().companies.all().order_by('name', '-created_at')


@require_POST
@login_required
def search_companies(request, organization_uuid):
    companies = []
    if request.method == 'POST':
        organization = get_object_or_404(Organization, pk=organization_uuid)
        search_query = request.POST.get('search_company')
        if search_query:
            companies = organization.companies.filter(
                name__icontains=search_query
            )
        return render(request,
                      'private/space/create/components/company/results.html',
                      {'companies': companies, 'search_query': search_query, 'organization': organization})
    return HttpResponseBadRequest()
