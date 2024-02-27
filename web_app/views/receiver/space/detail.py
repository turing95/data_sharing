from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from web_app.forms import SpaceForm, DetailRequestFormSet
from web_app.models import Space, Sender, GoogleDrive, GenericDestination
from web_app.views import SpaceFormView
from web_app.tasks.notifications import notify_invitation


class SpaceDetailFormView(SpaceFormView):
    template_name = "private/space/detail/base.html"
    form_class = SpaceForm

    def get_context_data(self, **kwargs):
        context = super(SpaceFormView, self).get_context_data(**kwargs)
        context['back'] = {'url': reverse_lazy('spaces',kwargs={'organization_uuid':self.get_organization().pk}), 'text': 'Back to Spaces'}
        if 'status' in self.request.GET:
            context = self.get_context_for_form(context, button_text='Save space',
                                                status=self.request.GET.get('status'))
        else:
            context['space'] = self.get_space()
            context['space_summary'] = True
        return context

    def dispatch(self, request, *args, **kwargs):
        # Call the parent dispatch method
        response = super(SpaceFormView, self).dispatch(request, *args, **kwargs)
        response["Cross-Origin-Opener-Policy"] = "unsafe-none"
        return response

    def handle_senders(self, senders_emails, space_instance):

        existing_senders = {sender.email: sender for sender in space_instance.senders.filter(is_active=True)}

        # Add or update senders
        for email in senders_emails:
            email = email.strip()
            if email in existing_senders:
                del existing_senders[email]
            else:
                sender, created = self.update_or_create_sender(email, space_instance)
                if space_instance.notify_invitation is True:
                    notify_invitation.delay(sender.pk)

        # Delete removed emails
        for email, sender in existing_senders.items():
            sender.is_active = False
            sender.save()
        for sender in space_instance.senders.all():
            if space_instance.deadline_notification_datetime is not None:
                sender.schedule_deadline_notification()

    def get_success_url(self):
        return self.request.path  # to summary page

    def get_space(self):
        if not self._space:
            pk = self.kwargs.get('space_uuid')
            self._space = get_object_or_404(Space, pk=pk,
                                            organization=self.kwargs.get('organization_uuid'),
                                            organization__in=self.request.user.organizations.all())
        return self._space

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_space()
        return kwargs

    def get_formset(self):
        formset = DetailRequestFormSet(self.request.POST or None,
                                       instance=self.get_space(),
                                       queryset=self.get_space().requests.order_by(
                                           'created_at'),
                                       form_kwargs=self.get_formset_kwargs())
        return formset

    def handle_formset(self, formset):
        formset.save()
        for req in formset:
            # Check if the current destination exists and if the folder ID matches the provided one.
            if req.instance.destination:
                if req.instance.destination.folder_id == req.cleaned_data.get('destination_id'):
                    if req.instance.destination.is_active is False:
                        # if inactive and same, create new
                        self.create_destination_from_form(req)
                else:
                    # If the folder ID doesn't match, create a new destination.
                    self.create_destination_from_form(req)

            else:
                # If no current destination exists, create a new one.
                self.create_destination_from_form(req)

            # Activate the instance in all cases after handling the destination.
            req.instance.is_active = True
            req.instance.save()
            if req.instance.file_types.exists():
                req.instance.file_types.clear()
            for file_type in req.cleaned_data.get('file_types'):
                req.instance.file_types.add(file_type)
