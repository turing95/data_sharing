from django.views.generic import FormView
from web_app.mixins import SubscriptionMixin
from django.urls import reverse
from web_app.forms import ContactForm
from web_app.mixins import ContactSideBarMixin, ContactMixin


class ContactDetailView(ContactSideBarMixin, SubscriptionMixin, ContactMixin, FormView):
    template_name = "private/contact/create.html"
    form_class = ContactForm

    def get_success_url(self):
        return reverse('contacts', kwargs={'organization_uuid': self.get_organization().pk})

    def form_valid(self, form):
        contact = form.save(commit=False)
        contact.organization = self.get_organization()
        contact.user = self.request.user
        contact.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['organization'] = self.get_organization()
        kwargs['instance'] = self.get_contact()
        return kwargs
