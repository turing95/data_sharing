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
from web_app.mixins import ContactSideBarMixin
import json


class ContactCreateView(OrganizationMixin, ContactSideBarMixin, SubscriptionMixin, FormView):
    template_name = "private/contact/create.html"
    form_class = ContactForm

    def get_success_url(self):
        return reverse('contacts', kwargs={'organization_uuid': self.get_organization().pk})

    def form_valid(self, form):
        contact = form.save(commit=False)
        contact.organization = self.get_organization()
        contact.user = self.request.user
        contact.save()
        if self.request.headers.get('HX-Request'):
            sender_uuid = self.request.GET.get('sender_uuid', None)
            if sender_uuid:
                # get sender or 404
                from web_app.models import Sender
                sender = get_object_or_404(Sender, pk=sender_uuid)
                sender.contact = contact
                sender.email = contact.email
                sender.save()
            messages.success(self.request, _('Contact created successfully'))
            form = ContactForm(organization=Organization.objects.get(pk=self.get_organization().pk))
            response = render(self.request,
                              'private/space/create/components/contacts/create_form.html',
                              {'form': form, 'from_htmx': True, 'organization_uuid': self.get_organization().pk, 'show_msg':True}
                              )

            response['HX-Trigger'] = "contactUpdated, closeModal"
    
            return response
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('HX-Request'):
            return render(self.request,
                          'private/space/create/components/contacts/create_form.html',
                          {'form': form, 'from_htmx': True, 'organization_uuid': self.get_organization().pk}
                          )
        return super().form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['organization'] = self.get_organization()
        return kwargs


@require_GET
@login_required
def contact_create_modal(request, organization_uuid):
    if request.method == 'GET':
        form = ContactForm(
            initial={'email': request.GET.get('query_search', None)},
            organization=Organization.objects.get(pk=organization_uuid))
        sender_uuid = request.GET.get('sender_uuid', None)
        return render(request,
                      'private/space/create/components/contacts/create_modal.html',
                      {'form': form, 'organization_uuid': organization_uuid, 'sender_uuid': sender_uuid})

    return HttpResponseBadRequest()
