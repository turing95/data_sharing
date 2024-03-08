from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_GET
from django.views.generic import FormView
from django.utils.translation import gettext_lazy as _
from web_app.mixins import SpaceSideBarMixin, RequestMixin, SubscriptionMixin
from web_app.models import Request, GenericDestination, File, Sender
from web_app.forms import RequestForm, FileSelectForm


class RequestDetailView(LoginRequiredMixin, SubscriptionMixin, RequestMixin, SpaceSideBarMixin, FormView):
    model = Request 
    form_class = RequestForm
    template_name = 'private/request/detail.html'
    _request = None  # Placeholder for the cached object

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['request_form'] = True
        context['back'] = {'url': reverse('receiver_space_detail', kwargs={'space_uuid': self.get_request().space.pk}),
                           'text': _('Back to Space')}
        context['submit_text'] = _('Save request')
        context['space'] = self.get_request().space
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
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
        # self.handle_destination(form)
        if self.request.headers.get('HX-Request'):
            messages.success(self.request, _('Request saved'))
            return render(self.request, 'components/messages.html', {'from_htmx': True})
        return super().form_valid(form)

    def form_invalid(self, form):
        # Check if the title field has errors
        title_errors = form.errors.get('title', None)
        # General error message for other form errors
        messages.error(self.request, _('Request not saved.'+ ' ' + ', '.join(title_errors)))

        if self.request.headers.get('HX-Request'):
            # Return specific partial for HTMX requests
            return render(self.request, 'components/messages.html', {'from_htmx': True, 'form': form})
        # Return the full form with errors for non-HTMX requests
        return self.render_to_response(self.get_context_data(form=form))


@login_required
@require_GET
def request_modal(request, request_uuid):
    upload_request = Request.objects.get(pk=request_uuid)

    sender = None
    public = False
    files = File.objects.filter(sender_event__request=upload_request)
    if request.GET.get('public'):
        public = True
        files = files.filter(sender_event__sender=None)
    elif request.GET.get('sender_uuid'):
        sender_uuid = request.GET.get('sender_uuid')
        sender = Sender.objects.get(pk=sender_uuid)
        files = files.filter(sender_event__sender=sender)
    changes_form = FileSelectForm(upload_request=upload_request, sender=sender, public=public)

    return render(request, 'private/space/detail/components/upload_request_modal.html',
                  {'req': upload_request,
                   'sender': sender,
                   'files': files,
                   'public': public,
                   'changes_form': changes_form})
