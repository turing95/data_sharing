import time
from django.http import Http404

from django.forms import formset_factory
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView
from web_app.models import Space, GenericDestination, GoogleDrive, Sender, SenderEvent, UploadRequest,File
from web_app.forms import FileForm, BaseFileFormSet


class SpaceDetailFormView(TemplateView):
    template_name = "public/sender_space_detail.html"

    _space = None
    _sender = None

    def get_formset(self):
        FileFormset = formset_factory(FileForm, formset=BaseFileFormSet, extra=self.get_space().requests.count())
        return FileFormset(self.request.POST or None, self.request.FILES or None,
                           form_kwargs={'space': self.get_space()})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_sender_detail_page'] = True
        context['space'] = self.get_space()
        context['sender'] = self.get_sender()
        context['formset'] = self.get_formset()
        context['remove_navbar'] = True
        return context

    def post(self, request, *args, **kwargs):
        formset = self.get_formset()
        if formset.is_valid():
            sender = self.get_sender()
            for form in formset:
                upload_request = UploadRequest.objects.get(pk=form.cleaned_data.get('request_uuid'))
                uploaded_files = form.cleaned_data.get('files')
                for uploaded_file in uploaded_files:
                    # Use the stored access token
                    google_drive_destination: GoogleDrive = upload_request.google_drive_destination

                    if upload_request.file_naming_formula is not None:
                        if sender is None:
                            file_name = upload_request.file_naming_formula.format(date=time.time(),
                                                                        original_name=uploaded_file.name)
                        else:
                            file_name = upload_request.file_naming_formula.format(date=time.time(),
                                                                        original_name=uploaded_file.name,
                                                                        email=sender.email)
                    else:
                        file_name = uploaded_file.name

                    google_drive_file = google_drive_destination.upload_file(uploaded_file, file_name)

                    SenderEvent.objects.create(sender=sender,
                                               request=upload_request,
                                               event_type=SenderEvent.EventType.FILE_UPLOADED,
                                               file=File.objects.create(original_name=uploaded_file.name,name=file_name, size=uploaded_file.size,
                                                                        file_type=uploaded_file.content_type,google_drive_url=google_drive_file.get('webViewLink')))
            return redirect(reverse('spaces'))
        return self.render_to_response(self.get_context_data(formset=formset))

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
                    self._sender = Sender.objects.get(pk=sender_id, is_active=True)
                except Sender.DoesNotExist:
                    raise Http404(f"Sender with id '{sender_id}' not found")

        return self._sender
