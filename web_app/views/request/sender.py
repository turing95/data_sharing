from django.contrib import messages
from django.http import Http404
from django.forms import formset_factory
from django.shortcuts import redirect
from django.views.generic import TemplateView
from web_app.models import Space, GenericDestination, Sender, SenderEvent, UploadRequest, File, Request
from web_app.forms import FileForm, BaseFileFormSet
from django.utils.translation import gettext_lazy as _


class RequestDetailView(TemplateView):
    template_name = "public/sender/request_detail.html"

    _request = None
    _sender = None

    def get_formset(self):
        FileFormset = formset_factory(FileForm, formset=BaseFileFormSet,
                                      extra=self.get_request().upload_requests.filter(is_active=True).count())
        return FileFormset(self.request.POST or None, self.request.FILES or None,
                           form_kwargs={'request': self.get_request()})

    def get_context_data(self, formset=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kezyy_request'] = self.get_request()
        context['space'] = self.get_request().space
        context['sender'] = self.get_sender()
        context['formset'] = formset or self.get_formset()
        return context

    def post(self, request, *args, **kwargs):
        formset = self.get_formset()
        if formset.is_valid():
            sender = self.get_sender()
            for form in formset:
                upload_request = UploadRequest.objects.get(pk=form.cleaned_data.get('request_uuid'))
                uploaded_files = form.cleaned_data.get('files')
                if uploaded_files:
                    destination: GenericDestination = upload_request.destination
                    sender_event = None
                    error = False
                    uploaded_files = uploaded_files if isinstance(uploaded_files, list) else [uploaded_files]
                    for uploaded_file in uploaded_files:
                        if sender_event is None:
                            sender_event = SenderEvent.objects.create(sender=sender,
                                                                      request=upload_request,
                                                                      space=upload_request.request.space,
                                                                      destination=destination,
                                                                      event_type=SenderEvent.EventType.FILE_UPLOADED,
                                                                      notes=form.cleaned_data.get('notes'))
                        file_name = upload_request.get_file_name_from_formula(sender, uploaded_file.name)
                        try:
                            file_url = destination.upload_file(uploaded_file, file_name)
                        except Exception:
                            error = True
                            messages.error(request, _(f"An error occurred while uploading file {uploaded_file.name}"))
                            continue
                        File.objects.create(original_name=uploaded_file.name,
                                            size=uploaded_file.size,
                                            file_type=uploaded_file.content_type,
                                            destination=destination,
                                            uid=file_url,
                                            sender_event=sender_event)
                    if sender_event is not None:
                        sender_event.notify(request.session.get('sender_upload_notification',False))
                    if not error:
                        messages.success(request, _(f"Your upload has completed"))
            return redirect(request.path)
        return self.render_to_response(self.get_context_data(formset=formset))

    def get_request(self):
        if not self._request:
            request_id = self.kwargs.get('request_uuid')
            sender = self.get_sender()

            filter_criteria = {
                'pk': request_id,
                'space__senders__uuid': sender.pk
            }
            try:
                self._request = Request.objects.get(**filter_criteria)
            except Request.DoesNotExist:
                raise Http404(_(f"No Space matches the given query: {filter_criteria}"))

        return self._request

    def get_sender(self):
        if not self._sender:
            sender_id = self.kwargs.get('sender_uuid', None)

            if sender_id is not None:
                try:
                    self._sender = Sender.objects.get(pk=sender_id, is_active=True)
                except Sender.DoesNotExist:
                    raise Http404(_(f"Sender with id '{sender_id}' not found"))

        return self._sender