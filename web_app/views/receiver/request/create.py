from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import FormView
from djstripe.mixins import SubscriptionMixin

from web_app.mixins import SpaceSideBarMixin, SpaceMixin
from web_app.models import UploadRequest, GenericDestination
from web_app.forms import RequestForm


class RequestCreateView(LoginRequiredMixin, SubscriptionMixin,SpaceMixin,SpaceSideBarMixin, FormView):
    model = UploadRequest
    form_class = RequestForm
    template_name = 'private/upload_request/create.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['request_form'] = True
        context['submit_text'] = 'Create request'
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        request_instance = form.save(commit=False)
        request_instance.space_id = self.kwargs.get('space_uuid')
        request_instance.save()
        GenericDestination.create_from_form(self.request, form)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('receiver_space_detail', kwargs={'space_uuid': self.kwargs.get('space_uuid')})
