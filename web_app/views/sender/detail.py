from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from web_app.models import Sender, Space
from web_app.tasks.notifications import bulk_notify_deadline as bulk_notify_deadline_task, \
    bulk_notify_invitation as bulk_notify_invitation_task
from django.utils.translation import gettext_lazy as _


@login_required
@require_POST
def toggle_sender_active(request, sender_uuid):
    sender = Sender.objects.get(pk=sender_uuid)
    sender.is_active = not sender.is_active
    sender.save()
    return HttpResponse(status=204)


@login_required
@require_POST
def notify_deadline(request, sender_uuid):
    sender = Sender.objects.get(pk=sender_uuid)
    # notify_deadline_task.delay(sender.pk)
    sender.notify_deadline()
    messages.success(request, _(f"{sender.email} notified"))
    return render(
        request,
        'components/messages.html',
        {'from_htmx': True}
    )


@login_required
@require_POST
def notify_invitation(request, sender_uuid):
    sender = Sender.objects.get(pk=sender_uuid)
    # notify_invitation_task.delay(sender.pk)
    sender.notify_invitation()
    messages.success(request, _("{sender.email} invited"))
    return render(
        request,
        'components/messages.html',
        {'from_htmx': True}
    )


@login_required
@require_POST
def bulk_notify_deadline(request, space_uuid):
    bulk_notify_deadline_task.delay(space_uuid)
    messages.success(request, _("Notification are being sent to all senders"))
    return render(
        request,
        'components/messages.html',
        {'from_htmx': True}
    )


@login_required
@require_POST
def bulk_notify_invitation(request, space_uuid):
    bulk_notify_invitation_task.delay(space_uuid)
    messages.success(request, _("Invitation are being sent to all senders"))
    return render(
        request,
        'components/messages.html',
        {'from_htmx': True}
    )


@login_required
@require_GET
def sender_row(request, sender_uuid):
    sender = Sender.objects.get(pk=sender_uuid)

    return render(request,
                  'private/space/detail/sender/sender_row.html',
                  {'sender': sender})


@require_POST
def sender_upload_notification(request):
    request.session['sender_upload_notification'] = request.POST['sender_upload_notification']
    return HttpResponse(status=204)


@login_required
@require_POST
def sender_notify(request, sender_uuid):
    sender = get_object_or_404(Sender, pk=sender_uuid)
    form = sender.notify_form(request.POST)
    if form.is_valid():
        sender.notify_space(form.cleaned_data['subject'], form.cleaned_data['content'])
        response = HttpResponse()
        response['HX-Trigger'] = 'closeModal'
        return response
    else:
        return render(request, 'private/space/detail/sender/notify_form.html', {
            'sender': sender,
            'form': form
        })
