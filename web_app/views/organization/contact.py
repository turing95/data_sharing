from django.views.generic import ListView, CreateView, FormView
from web_app.mixins import OrganizationMixin, SideBarMixin, SubscriptionMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST, require_GET
from web_app.forms import ContactForm
from web_app.models import Contact, Organization
from django.utils.translation import gettext_lazy as _


class ContactSideBarMixin(SideBarMixin):
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['sidebar']['contact'] = True
        return data


class ContactListView(OrganizationMixin, ContactSideBarMixin, SubscriptionMixin, ListView):
    template_name = "private/contact/list.html"
    paginate_by = 12

    def get_queryset(self):
        return self.get_organization().contacts.all().order_by('first_name', 'last_name', 'created_at')


class ContactCreateView(OrganizationMixin, SideBarMixin, SubscriptionMixin, FormView):
    template_name = "private/contact/create.html"
    form_class = ContactForm

    def get_success_url(self):
        return reverse('contacts', kwargs={'organization_uuid': self.get_organization().pk})

    def form_valid(self, form):
        contact = form.save(commit=False)
        contact.organization = self.get_organization()
        contact.save()
        return super().form_valid(form)


@require_POST
@login_required
def search_contacts(request, organization_uuid):
    contacts = []
    if request.method == 'POST':
        organization = get_object_or_404(Organization, pk=organization_uuid)
        search_query = request.POST.get('search-contacts')
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


@require_GET
@login_required
def contact_create_modal(request, organization_uuid):
    if request.method == 'GET':
        form = ContactForm(request=request,
                           initial={'email': request.GET.get('search-contacts', None)},
                           organization=Organization.objects.get(pk=organization_uuid))
        return render(request,
                      'private/space/create/components/contacts/create_modal.html',
                      {'form': form, 'organization_uuid': organization_uuid})

    return HttpResponseBadRequest()


@require_POST
@login_required
def contact_create(request, organization_uuid):
    if request.method == 'POST':
        form = ContactForm(request.POST, request=request,organization=Organization.objects.get(pk=organization_uuid))
        if form.is_valid():
            instance = Contact.objects.filter(email=form.cleaned_data['email'],
                                              organization_id=organization_uuid).first()
            if instance:
                instance.first_name = form.cleaned_data['first_name']
                instance.last_name = form.cleaned_data['last_name']
                instance.company = form.cleaned_data['company']
                instance.organization_id = organization_uuid
                instance.save()
            else:
                contact = form.save(commit=False)
                contact.user = request.user
                contact.organization_id = organization_uuid
                contact.save()
            messages.success(request, _('Contact created successfully'))
            status = 200
            form = ContactForm(request=request,organization=Organization.objects.get(pk=organization_uuid))
        else:
            messages.error(request, _('Error creating contact. Please try again.'))
            status = 400
            form = form
        if request.headers.get('HX-Request'):
            return render(request,
                          'private/space/create/components/contacts/create_form.html',
                          {'form': form, 'show_msg': True, 'from_htmx': True, 'organization_uuid': organization_uuid},
                          status=status
                          )
        else:
            if status == 200:
                return redirect(reverse('contacts', kwargs={'organization_uuid': organization_uuid}))
            return render(request,
                          "private/contact/create.html",
                          {'form': form, 'organization_uuid': organization_uuid}
                          )
    return HttpResponseNotFound()