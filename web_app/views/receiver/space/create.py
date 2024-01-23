from django.conf import settings
from django.shortcuts import redirect
from djstripe.models import Customer
from djstripe.settings import djstripe_settings

from web_app.forms import SpaceForm, RequestFormSet
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from web_app.models import Sender, GoogleDrive, UploadRequest, FileType, Space, OneDrive, GenericDestination
from django.db import transaction
from web_app.tasks.notifications import notify_invitation
from web_app.mixins import SubscriptionMixin


class SpaceFormView(LoginRequiredMixin,SubscriptionMixin, FormView):
    template_name = "private/space/create/base.html"
    form_class = SpaceForm
    success_url = reverse_lazy('spaces')
    _space = None  # Placeholder for the cached object

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        # Call the parent dispatch method
        customer, _created = Customer.get_or_create(
            subscriber=djstripe_settings.subscriber_request_callback(self.request)
        )
        if not customer.subscription and request.user.spaces.filter(is_deleted=False).count() >= settings.MAX_FREE_SPACES:
            return redirect('create_checkout_session')
        response = super().dispatch(request, *args, **kwargs)

        response["Cross-Origin-Opener-Policy"] = "unsafe-none"
        return response

    def get_success_url(self):
        if self._space is not None:
            return reverse_lazy('receiver_space_detail', kwargs={'space_uuid': self._space.uuid})
        return super().get_success_url()

    def get_formset_kwargs(self):
        kwargs = {'custom_user':self.request.custom_user}
        return kwargs
    def get_context_for_form(self, data, button_text='Create space', **kwargs):
        data['back'] = {'url': reverse_lazy('spaces'), 'text': 'Back to Spaces'}
        data['space_form'] = True
        data['file_name_tags'] = {'tags': [tag[1] for tag in UploadRequest.FileNameTag.choices]}
        data['file_types'] = FileType.objects.filter(group=False)
        data['requests'] = self.get_formset()
        data['submit_text'] = button_text
        data.update(kwargs)
        return data

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        return self.get_context_for_form(data)

    def get_formset(self):
        return RequestFormSet(self.request.POST or None,form_kwargs=self.get_formset_kwargs())

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

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

    @staticmethod
    def handle_senders(emails, space_instance:Space):
        for email in emails:
            sender = Sender.objects.create(email=email, space=space_instance)
            if space_instance.notify_invitation is True:
                notify_invitation.delay(sender.pk)
            if space_instance.deadline_notification_datetime is not None:
                sender.schedule_deadline_notification()


    @staticmethod
    def handle_formset(formset):
        formset.save()
        for req in formset:
            GenericDestination.create_from_folder_id(req.instance,req.cleaned_data.get('destination_type'), req.cleaned_data.get('destination_id'))
            for file_type in req.cleaned_data.get('file_types'):
                req.instance.file_types.add(file_type)
