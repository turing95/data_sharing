from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from web_app.models import Sender


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
