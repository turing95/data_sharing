from django.shortcuts import redirect

from web_app.forms import SpaceForm
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import AccessMixin
from web_app.models import Sender, Space, Contact
from web_app.tasks.notifications import notify_invitation
from web_app.mixins import SubscriptionMixin, OrganizationMixin, SideBarMixin
from django.utils.translation import gettext_lazy as _


class SpaceCreateView(AccessMixin, SubscriptionMixin, OrganizationMixin,SideBarMixin, FormView):
    form_class = SpaceForm
    _space = None  # Placeholder for the cached object
    template_name = "private/space/create/base.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.can_create_space:
            return redirect('create_checkout_session')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        if self._space is not None:
            return reverse_lazy('receiver_space_detail', kwargs={'space_uuid': self._space.uuid})
        return super().get_success_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['space_form'] = True
        context['submit_text'] = _('Create space')
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['organization'] = self.get_organization()
        return kwargs

    def form_valid(self, form):
        space_instance = form.save(commit=False)
        space_instance.user = self.request.user
        space_instance.organization = self.get_organization()
        space_instance.save()
        self._space = space_instance
        self.handle_senders(form.cleaned_data.get('senders_emails', []), space_instance)
        return super().form_valid(form)

    def handle_senders(self, emails, space_instance: Space):
        for email in emails:
            contact, created = Contact.objects.get_or_create(email=email, user=self.request.user)
            sender, created = Sender.objects.update_or_create(email=contact.email, contact=contact,
                                                              space=space_instance, defaults={'is_active': True})
            if space_instance.notify_invitation is True:
                notify_invitation.delay(sender.pk)
            if space_instance.deadline_notification_datetime is not None:
                sender.schedule_deadline_notification()
