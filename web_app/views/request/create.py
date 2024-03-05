from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import FormView

from web_app.mixins import SpaceSideBarMixin, SpaceMixin, SubscriptionMixin
from web_app.models import UploadRequest, GenericDestination, Space, Request
from web_app.forms import RequestForm


class RequestCreateView(LoginRequiredMixin, SubscriptionMixin, SpaceMixin, SpaceSideBarMixin, FormView):
    model = UploadRequest
    form_class = RequestForm
    template_name = 'private/request/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['back'] = {
            'url': reverse('receiver_space_detail', kwargs={'space_uuid': self.kwargs.get('space_uuid')}),
            'text': 'Back to Space'}
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


@login_required
@require_GET
def request_create(request, space_uuid):
    space = get_object_or_404(Space, pk=space_uuid, organization__in=request.user.organizations.all())
    space_request = Request.objects.create(space=space, title='Untitled')
    return redirect('request_detail', request_uuid=space_request.pk)
