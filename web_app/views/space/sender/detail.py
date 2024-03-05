from django.contrib import messages
from django.http import Http404
from django.forms import formset_factory
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView
from web_app.models import Space, GenericDestination, Sender, SenderEvent, UploadRequest, File
from web_app.forms import FileForm, BaseFileFormSet
from django.utils.translation import gettext_lazy as _


class SpaceDetailView(TemplateView):
    template_name = "public/sender/space_detail.html"

    _space = None
    _sender = None

    def get_context_data(self, formset=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['space'] = self.get_space()
        context['sender'] = self.get_sender()
        return context

    def get_space(self):
        if not self._space:
            space_id = self.kwargs.get('space_uuid')
            sender = self.get_sender()

            filter_criteria = {
                'pk': space_id,
                'is_deleted': False,
                'senders__uuid': sender.pk
            }
            self._space = get_object_or_404(Space, **filter_criteria)
        return self._space

    def get_sender(self):
        if not self._sender:
            sender_id = self.kwargs.get('sender_uuid', None)

            if sender_id is not None:
                try:
                    self._sender = Sender.objects.get(pk=sender_id, is_active=True)
                except Sender.DoesNotExist:
                    raise Http404(_(f"Sender with id '{sender_id}' not found"))

        return self._sender
