from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST
from django.views.generic import FormView, TemplateView
from django.utils.translation import gettext_lazy as _
from web_app.mixins import SpaceSideBarMixin, RequestMixin, SubscriptionMixin, RequestTabMixin
from web_app.models import Request, File, Sender
from web_app.forms import FileSelectForm


class RequestEditView(LoginRequiredMixin, SubscriptionMixin, RequestMixin, SpaceSideBarMixin, RequestTabMixin,
                      TemplateView):
    template_name = 'private/request/edit.html'
    _request = None  # Placeholder for the cached object

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['request_form'] = True
        context['request_tab']['edit']['active'] = True
        context['inputs_tooltip_content'] =_("Add input fields to your request below")
        context['space'] = self.get_request().space
        return context


@login_required
@require_POST
def request_title_update(request, request_uuid):
    if request.method == 'POST':
        kezyy_request = get_object_or_404(Request, pk=request_uuid)
        form = kezyy_request.title_form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Request saved'))
            return render(request, 'private/request/request_title_form.html',
                          {'from_htmx': True, 'form': kezyy_request.title_form()})
        messages.error(request, form.errors)
        return render(request, 'private/request/request_title_form.html',
                      {'from_htmx': True, 'form': kezyy_request.title_form()})
    return HttpResponseBadRequest()


@login_required
@require_POST
def request_instructions_update(request, request_uuid):
    if request.method == 'POST':
        kezyy_request = get_object_or_404(Request, pk=request_uuid)
        form = kezyy_request.instructions_form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Request saved'))
            return render(request, 'private/request/request_instructions_form.html',
                          {'from_htmx': True, 'form': kezyy_request.instructions_form()})
        messages.error(request, form.errors)
        return render(request, 'private/request/request_instructions_form.html',
                      {'from_htmx': True, 'form': kezyy_request.instructions_form()})
    return HttpResponseBadRequest()


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
