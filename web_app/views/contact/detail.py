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
from web_app.mixins import ContactSideBarMixin, ContactMixin



class ContactDetailView(ContactSideBarMixin, SubscriptionMixin, ContactMixin,  FormView):
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
            messages.success(self.request, _('Contact created successfully'))
            form = ContactForm(contact=self.contact)
            return render(self.request,
                          'private/space/create/components/contacts/create_form.html',
                          {'form': form, 'from_htmx': True, 'organization_uuid': self.get_organization().pk}
                          )
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
        kwargs['contact'] = self.get_contact()
        kwargs['organization'] = self.get_organization()
        return kwargs
