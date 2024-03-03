from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.utils.translation import gettext_lazy as _

from web_app.forms import SpaceForm, DetailRequestFormSet
from web_app.mixins import SubscriptionMixin
from web_app.models import Space, UploadRequest, GenericDestination, Contact, Sender
from web_app.tasks.notifications import notify_invitation


class SpaceDetailFormView(LoginRequiredMixin, SubscriptionMixin, FormView):
    template_name = "private/space/detail/base.html"
    form_class = SpaceForm
    _space = None  # Placeholder for the cached object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back'] = {
            'url': reverse_lazy('spaces', kwargs={'organization_uuid': self.get_space().organization.pk}),
            'text': _('Back to Spaces')}

        if 'status' in self.request.GET:
            context['space_form'] = True
            context['file_name_tags'] = {'tags': [tag[1] for tag in UploadRequest.FileNameTag.choices]}
            context['requests'] = self.get_formset()
            context['submit_text'] = _('Save space')
            context['status'] = self.request.GET.get('status')
            context['organization'] = self.get_space().organization
        else:
            context['space'] = self.get_space()
            context['space_summary'] = True
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        formset = self.get_formset()

        if form.is_valid():
            space_instance = form.save(commit=False)
            space_instance.user = request.user
            formset.instance = space_instance

            if formset.is_valid():
                with transaction.atomic():
                    space_instance.save()
                    self._space = space_instance
                    self.handle_senders(form.cleaned_data.get('senders_emails', []), space_instance)
                    self.handle_formset(formset)
                return self.form_valid(form)
        return self.form_invalid(form)

    def get_success_url(self):
        return self.request.path  # to summary page

    def get_space(self):
        if not self._space:
            self._space = get_object_or_404(Space, pk=self.kwargs.get('space_uuid'), organization__in=self.request.user.organizations.all())
        return self._space

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_space()
        kwargs['organization'] = self.get_space().organization
        return kwargs

    def get_formset(self):
        formset = DetailRequestFormSet(self.request.POST or None,
                                       instance=self.get_space(),
                                       queryset=self.get_space().requests.order_by(
                                           'created_at'),
                                       form_kwargs={'request': self.request})
        return formset

    def handle_senders(self, senders_emails, space_instance: Space):

        existing_senders = {sender.email: sender for sender in space_instance.senders.filter(is_active=True)}

        # Add or update senders
        for email in senders_emails:
            email = email.strip()
            if email in existing_senders:
                del existing_senders[email]
            else:
                contact, created = Contact.objects.get_or_create(email=email, user=self.request.user)
                sender, created = Sender.objects.update_or_create(email=contact.email, contact=contact,
                                                                  space=space_instance, defaults={'is_active': True})
                if space_instance.notify_invitation is True:
                    notify_invitation.delay(sender.pk)

        # Delete removed emails
        for email, sender in existing_senders.items():
            if sender.events.exists():
                sender.is_active = False
                sender.save()
            else:
                sender.delete()
        for sender in space_instance.senders.all():
            if space_instance.deadline_notification_datetime is not None:
                sender.schedule_deadline_notification()

    def handle_formset(self, formset):
        formset.save()
        for req in formset:
            # Check if the current destination exists and if the folder ID matches the provided one.
            if req.instance.destination:
                if req.instance.destination.folder_id == req.cleaned_data.get('destination_id'):
                    if req.instance.destination.is_active is False:
                        # if inactive and same, create new
                        GenericDestination.create_from_form(self.request, req)
                else:
                    # If the folder ID doesn't match, create a new destination.
                    GenericDestination.create_from_form(self.request, req)

            else:
                # If no current destination exists, create a new one.
                GenericDestination.create_from_form(self.request, req)

            # Activate the instance in all cases after handling the destination.
            req.instance.is_active = True
            req.instance.save()
            if req.instance.file_types.exists():
                req.instance.file_types.clear()
            for file_type in req.cleaned_data.get('file_types', []):
                req.instance.file_types.add(file_type)
