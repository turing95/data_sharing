from django.views.generic import ListView
from web_app.mixins import OrganizationMixin, SubscriptionMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from web_app.mixins import ContactSideBarMixin
from web_app.models import Organization


class ContactListView(OrganizationMixin, ContactSideBarMixin, SubscriptionMixin, ListView):
    template_name = "private/contact/list.html"
    paginate_by = 2

    def get_queryset(self):
        return self.get_organization().contacts.all().order_by('first_name', 'last_name', 'created_at')


@require_POST
@login_required
def search_contacts(request, organization_uuid):
    contacts = []
    if request.method == 'POST':
        organization = get_object_or_404(Organization, pk=organization_uuid)
        search_query = request.POST.get('email')
        if search_query:
            contacts = organization.contacts.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(company__name__icontains=search_query)
            )
        return render(request,
                      'private/space/create/components/contacts/results.html',
                      {'contacts': contacts})
    return HttpResponseBadRequest()
