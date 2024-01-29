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
        context['back'] = {'url': reverse_lazy('spaces'), 'text': 'Back to Spaces'}
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
                sender, created = Sender.objects.update_or_create(email=email, space=space_instance, defaults={'is_active': True})
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
            self._space = get_object_or_404(Space, pk=pk)
        return self._space

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_space()
        return kwargs

    def get_formset_kwargs(self):
        kwargs= super().get_formset_kwargs()
        kwargs['access_token'] = self.get_space()
        return kwargs
    def get_formset(self):
        formset = DetailRequestFormSet(self.request.POST or None,
                                       instance=self.get_space(),
                                       queryset=self.get_space().requests.filter(is_deleted=False).order_by(
                                           'created_at'),
                                       form_kwargs=self.get_formset_kwargs())
        return formset

    @staticmethod
    def handle_formset(formset):
        formset.save()
        for req in formset:
            if (req.instance.destination is not None and req.instance.destination.folder_id != req.cleaned_data.get('destination_id')) or req.instance.destination is None:
                GenericDestination.create_from_folder_id(req.instance, req.cleaned_data.get('destination_type'), req.cleaned_data.get('destination_id'))
            if req.instance.file_types.exists():
                req.instance.file_types.clear()
            for file_type in req.cleaned_data.get('file_types'):
                req.instance.file_types.add(file_type)
