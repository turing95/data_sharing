from collections import defaultdict

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_POST
from web_app.forms import FileSelectForm
from web_app.models import File, UploadRequest, Sender
from django.http import HttpResponseBadRequest
from django.utils.translation import gettext_lazy as _


@require_POST
@login_required
def request_changes(request, request_uuid):
    if request.method == 'POST':
        upload_request = UploadRequest.objects.get(pk=request_uuid)
        sender_uuid = request.GET.get('sender', None)
        public = request.GET.get('public', None)
        sender = Sender.objects.filter(pk=sender_uuid).first()
        changes_form = FileSelectForm(request.POST, sender=sender, public=public, upload_request=upload_request)
        events = upload_request.events.filter(sender=sender)
        if changes_form.is_valid():
            files = changes_form.cleaned_data['files']
            notes = changes_form.cleaned_data['notes']
            files_by_senders = defaultdict(list)
            for file in files:
                files_by_senders[file.sender_event.sender].append(file)
                file.status = File.FileStatus.REJECTED
                file.save()
            # Notify each sender about the changes request
            for tmp_sender, sender_files in files_by_senders.items():
                tmp_sender.notify_changes_request(upload_request, sender_files, notes)
            changes_form = FileSelectForm(sender=sender, public=public, upload_request=upload_request)
            messages.success(request, _('Changes requested successfully'))
        return render(request, 'private/space/detail/components/changes_form.html',
                      {'req': upload_request, 'sender': sender, 'upload_events': events, 'changes_form': changes_form,
                       'show_msg': True})
    return HttpResponseBadRequest()


@require_POST
@login_required
def accept_all(request, request_uuid):
    if request.method == 'POST':
        upload_request = UploadRequest.objects.get(pk=request_uuid)
        sender_uuid = request.GET.get('sender', None)
        public = request.GET.get('public', None)
        sender = Sender.objects.filter(pk=sender_uuid).first()
        files = File.objects.filter(sender_event__request=upload_request)
        if public:
            files = files.filter(sender_event__sender__isnull=True)
        elif sender:
            files = files.filter(sender_event__sender=sender)
        files.update(
            status=File.FileStatus.ACCEPTED)
        messages.success(request, _('All files accepted successfully'))
        return render(
            request,
            'components/messages.html',
            {'from_htmx': True}
        )
    return HttpResponseBadRequest()


@require_POST
@login_required
def accept_all(request, request_uuid):
    if request.method == 'POST':
        upload_request = UploadRequest.objects.get(pk=request_uuid)
        sender_uuid = request.GET.get('sender', None)
        public = request.GET.get('public', None)
        sender = Sender.objects.filter(pk=sender_uuid).first()
        files = File.objects.filter(sender_event__request=upload_request)
        if public:
            files = files.filter(sender_event__sender__isnull=True)
        elif sender:
            files = files.filter(sender_event__sender=sender)
        files.update(
            status=File.FileStatus.ACCEPTED)
        messages.success(request, _('All files accepted successfully'))
        return render(
            request,
            'components/messages.html',
            {'from_htmx': True}
        )
    return HttpResponseBadRequest()


@require_POST
@login_required
def accept_single(request,file_uuid):
    if request.method == 'POST':
        File.objects.filter(pk=file_uuid).update(status=File.FileStatus.ACCEPTED)
        messages.success(request, _('File accepted successfully'))
        return render(
            request,
            'components/messages.html',
            {'from_htmx': True}
        )
    return HttpResponseBadRequest()
