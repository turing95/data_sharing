from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_POST
from web_app.forms import FileSelectForm
from web_app.models import File, UploadRequest, Sender


class HttpBadRequest:
    pass


@require_POST
@login_required
def request_changes(request,request_uuid,sender_uuid):
    if request.method == 'POST':
        upload_request = UploadRequest.objects.get(pk=request_uuid)
        sender = Sender.objects.get(pk=sender_uuid)
        changes_form = FileSelectForm(request.POST,sender=sender,upload_request=upload_request)
        events = upload_request.events.filter(sender=sender)
        if changes_form.is_valid():
            files = changes_form.cleaned_data['files']
            notes = changes_form.cleaned_data['notes']

            for file in files:
                file.status = File.FileStatus.REJECTED
                file.save()
            messages.success(request, 'Changes requested successfully')
        return render(request, 'private/space/detail/components/changes_form.html',
                      {'req': upload_request, 'sender': sender, 'upload_events': events, 'changes_form': changes_form,'show_msg': True})
    return HttpBadRequest()
