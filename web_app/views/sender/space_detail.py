from django.http import Http404

from web_app.forms import SpaceDetailForm
from django.views.generic.edit import FormView
from web_app.models import Space, GenericDestination, GoogleDrive, Sender, SenderEvent
from django.urls import reverse_lazy

from django import forms
import time


class SpaceDetailFormView(FormView):
    template_name = "public/sender_space_detail.html"
    form_class = SpaceDetailForm
    success_url = reverse_lazy('spaces')
    _space = None
    _sender = None

    def form_valid(self, form):
        space = self.get_space()
        sender = self.get_sender()
        for space_req in space.requests.all():
            field_name = f'file_{space_req.pk}'
            uploaded_file = form.cleaned_data.get(field_name)
            if uploaded_file:
                # Use the stored access token
                google_drive_destination: GoogleDrive = GenericDestination.objects.get(request=space_req).related_object

                if space_req.file_name is not None:
                    if sender is None:
                        file_name = space_req.file_name.format(date=time.time(), original_name=uploaded_file.name)
                    else:
                        file_name = space_req.file_name.format(date=time.time(), original_name=uploaded_file.name,
                                                               email=sender.email)
                else:
                    file_name = uploaded_file.name

                google_drive_destination.upload_file(uploaded_file, file_name)
                SenderEvent.objects.create(sender=sender,
                                           request=space_req,
                                           event_type=SenderEvent.EventType.FILE_UPLOADED,
                                           data={'file_name': file_name,
                                                 'file_type': uploaded_file.content_type,
                                                 'size': uploaded_file.size})
        return super().form_valid(form)

    def get_space(self):
        if not self._space:
            space_id = self.kwargs.get('space_uuid')
            sender = self.get_sender()

            filter_criteria = {
                'pk': space_id,
                'is_active': True
            }
            if sender is not None:
                filter_criteria['senders__uuid'] = sender.pk
            try:
                self._space = Space.objects.get(**filter_criteria)
            except Space.DoesNotExist:
                raise Http404(f"No Space matches the given query: {filter_criteria}")

        return self._space

    def get_sender(self):
        if not self._sender:
            sender_id = self.kwargs.get('sender_uuid', None)

            if sender_id is not None:
                try:
                    self._sender = Sender.objects.get(pk=sender_id,is_active=True)
                except Sender.DoesNotExist:
                    raise Http404(f"Sender with id '{sender_id}' not found")

        return self._sender

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        space: Space = self.get_space()

        for index, space_req in enumerate(space.requests.all()):
            form.fields[f'file_{space_req.pk}'] = forms.FileField()

        return form
