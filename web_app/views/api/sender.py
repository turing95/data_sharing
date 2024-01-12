from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render
from django.views.decorators.http import require_POST

from web_app.models import Sender


@login_required
@require_POST
def toggle_sender_active(request, sender_uuid):
    sender = Sender.objects.get(pk=sender_uuid)
    sender.is_active = not sender.is_active
    sender.save()
    return render(
        request,
        'private/space/detail/components/sender_row.html',
        {'sender': sender, 'space': sender.space}
    )


@login_required
@require_POST
def notify_sender(request, sender_uuid):
    sender = Sender.objects.get(pk=sender_uuid)
    sender.notify_deadline()
    messages.success(request, f"Sender {sender.email} notified")
    return render(
        request,
        'components/messages.html'
    )
