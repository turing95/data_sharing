from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST, require_GET
from web_app.models import Sender, Space
from web_app.tasks.notifications import bulk_notify_deadline as bulk_notify_deadline_task, bulk_notify_invitation as bulk_notify_invitation_task

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
    messages.success(request, f"{sender.email} notified")
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
    messages.success(request, f"{sender.email} invited")
    return render(
        request,
        'components/messages.html',
        {'from_htmx': True}
    )


@login_required
@require_POST
def bulk_notify_deadline(request, space_uuid):
    bulk_notify_deadline_task.delay(space_uuid)
    messages.success(request, "Notification are being sent to all senders")
    return render(
        request,
        'components/messages.html',
        {'from_htmx': True}
    )


@login_required
@require_POST
def bulk_notify_invitation(request, space_uuid):
    bulk_notify_invitation_task.delay(space_uuid)
    messages.success(request, "Invitation are being sent to all senders")
    return render(
        request,
        'components/messages.html',
        {'from_htmx': True}
    )


@login_required
@require_GET
def sender_modal(request, sender_uuid):
    sender = Sender.objects.get(pk=sender_uuid)

    return render(request, 'private/space/detail/components/sender_modal.html',
                  {'sender': sender})


@login_required
@require_GET
def sender_info(request, sender_uuid):
    sender = Sender.objects.get(pk=sender_uuid)

    return render(request, 'private/space/detail/components/sender_info.html',
                  {'sender': sender})


@login_required
@require_GET
def sender_row(request, sender_uuid):
    sender = Sender.objects.get(pk=sender_uuid)

    return render(request, 'private/space/detail/components/sender_row.html',
                  {'sender': sender})


@login_required
@require_GET
def all_senders_modal(request, space_uuid):
    space = Space.objects.get(pk=space_uuid)

    return render(request, 'private/space/detail/components/all_senders_modal.html',
                  {'space': space})
