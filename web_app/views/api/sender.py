from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_POST, require_GET

from web_app.forms.widgets import SenderToggle
from web_app.models import Sender, Space



@login_required
@require_POST
def toggle_sender_active(request, sender_uuid):
    sender = Sender.objects.get(pk=sender_uuid)
    sender.is_active = not sender.is_active
    sender.save()
    return HttpResponse()


@login_required
@require_POST
def notify_deadline(request, sender_uuid):
    sender = Sender.objects.get(pk=sender_uuid)
    #notify_deadline_task.delay(sender.pk)
    sender.notify_deadline()
    messages.success(request, f"{sender.email} notified")
    return render(
        request,
        'components/messages.html'
    )


@login_required
@require_POST
def notify_invitation(request, sender_uuid):
    sender = Sender.objects.get(pk=sender_uuid)
    #notify_invitation_task.delay(sender.pk)
    sender.notify_invitation()
    messages.success(request, f"{sender.email} invited")
    return render(
        request,
        'components/messages.html'
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
