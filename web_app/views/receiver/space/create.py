from django.shortcuts import redirect
from web_app.forms import SpaceForm, RequestFormSet
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import AccessMixin
from web_app.models import Sender, UploadRequest, FileType, Space, GenericDestination, Contact
from django.db import transaction
from web_app.tasks.notifications import notify_invitation
from web_app.mixins import SubscriptionMixin, OrganizationMixin


class SpaceFormView(AccessMixin, SubscriptionMixin, OrganizationMixin, FormView):
    template_name = "private/space/create/base.html"
    form_class = SpaceForm
    success_url = reverse_lazy('spaces')
    _space = None  # Placeholder for the cached object
    _organization = None  # Placeholder for the cached object

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.can_create_space:
            return redirect('create_checkout_session')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        if self._space is not None:
            return reverse_lazy('receiver_space_detail', kwargs={'space_uuid': self._space.uuid,
                                                                 'organization_uuid': self.get_organization().pk})
        return super().get_success_url()

    def get_context_for_form(self, data, button_text='Create space', **kwargs):
        data['back'] = {'url': reverse_lazy('spaces', kwargs={'organization_uuid': self.get_organization().pk}),
                        'text': 'Back to Spaces'}
        data['space_form'] = True
        data['file_name_tags'] = {'tags': [tag[1] for tag in UploadRequest.FileNameTag.choices]}
        data['requests'] = self.get_formset()
        data['submit_text'] = button_text
        data.update(kwargs)
        return data

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        return self.get_context_for_form(data)

    def get_formset(self):
        return RequestFormSet(self.request.POST or None, form_kwargs={'request': self.request})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        formset = self.get_formset()

        if form.is_valid():
            space_instance = form.save(commit=False)
            space_instance.user = request.user
            space_instance.organization = self.get_organization()
            formset.instance = space_instance

            if formset.is_valid():
                with transaction.atomic():
                    space_instance.save()
                    self._space = space_instance
                    self.handle_senders(form.cleaned_data.get('senders_emails', []), space_instance)
                    self.handle_formset(formset)
                return self.form_valid(form)
        return self.form_invalid(form)

    def handle_senders(self, emails, space_instance: Space):
        for email in emails:
            contact, created = Contact.objects.get_or_create(email=email, user=self.request.user)
            sender, created = Sender.objects.update_or_create(email=contact.email, contact=contact,
                                                              space=space_instance, defaults={'is_active': True})
            if space_instance.notify_invitation is True:
                notify_invitation.delay(sender.pk)
            if space_instance.deadline_notification_datetime is not None:
                sender.schedule_deadline_notification()

    def handle_formset(self, formset):
        formset.save()
        for req in formset:
            GenericDestination.create_from_form(self.request,req)
            for file_type in req.cleaned_data.get('file_types', []):
                req.instance.file_types.add(file_type)
