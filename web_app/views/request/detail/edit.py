from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_GET
from django.views.generic import FormView
from django.utils.translation import gettext_lazy as _
from web_app.mixins import SpaceSideBarMixin, RequestMixin, SubscriptionMixin, RequestTabMixin
from web_app.models import Request, File, Sender
from web_app.forms import RequestForm, FileSelectForm


class RequestEditView(LoginRequiredMixin, SubscriptionMixin, RequestMixin, SpaceSideBarMixin, RequestTabMixin, FormView):
    model = Request
    form_class = RequestForm
    template_name = 'private/request/edit.html'
    _request = None  # Placeholder for the cached object

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['request_form'] = True
        context['request_tab']['edit']['active'] = True
        context['submit_text'] = _('Save request')
        context['space'] = self.get_request().space
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_request()
        return kwargs

    def form_valid(self, form):
        form.save()
        if self.request.headers.get('HX-Request'):
            messages.success(self.request, _('Request saved'))
            return render(self.request, 'private/request/request_form.html',
                          {'from_htmx': True, 'form': self.form_class(instance=self.get_request())})
        return super().form_valid(form)

    def form_invalid(self, form):

        if self.request.headers.get('HX-Request'):
            title_errors = form.errors.get('title', None)
            messages.error(self.request, title_errors)
            return render(self.request, 'private/request/request_form.html',
                          {'from_htmx': True, 'form': self.form_class(instance=self.get_request())})
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
