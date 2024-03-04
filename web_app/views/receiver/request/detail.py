from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import FormView
from djstripe.mixins import SubscriptionMixin

from web_app.mixins import SpaceMixin,SpaceSideBarMixin
from web_app.models import UploadRequest, GenericDestination
from web_app.forms import RequestForm


class RequestDetailView(LoginRequiredMixin, SubscriptionMixin,SpaceSideBarMixin, FormView):
    model = UploadRequest
    form_class = RequestForm
    template_name = 'private/upload_request/create.html'
    _request = None  # Placeholder for the cached object

    def get_request(self):
        if not self._request:
            self._request = get_object_or_404(UploadRequest, pk=self.kwargs.get('request_uuid'))
        return self._request

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['request_form'] = True
        context['submit_text'] = 'Save request'
        context['space'] = self.get_request().space
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['instance'] = self.get_request()
        return kwargs

    def handle_destination(self, form):
        if form.instance.destination:
            if form.instance.destination.folder_id == form.cleaned_data.get('destination_id'):
                if form.instance.destination.is_active is False:
                    # if inactive and same, create new
                    GenericDestination.create_from_form(self.request, form)
            else:
                # If the folder ID doesn't match, create a new destination.
                GenericDestination.create_from_form(self.request, form)

        else:
            # If no current destination exists, create a new one.
            GenericDestination.create_from_form(self.request, form)

        # Activate the instance in all cases after handling the destination.
        form.instance.is_active = True
        form.instance.save()

    def form_valid(self, form):
        form.save()
        self.handle_destination(form)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('receiver_space_detail', kwargs={'space_uuid': self.get_request().space.pk})
