from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from utils.render_block import render_block_to_string
from web_app.models import Space, Sender, UploadRequest


@require_POST
def toggle_space_active(request, space_uuid):
    space = Space.objects.get(pk=space_uuid)
    space.is_active = not space.is_active
    space.save()
    return HttpResponse(
        render_block_to_string('private/space/detail/components/summary.html', 'details', {'space': space}, request))


@require_POST
def toggle_space_public(request, space_uuid):
    space = Space.objects.get(pk=space_uuid)
    space.is_public = not space.is_public
    space.save()
    return HttpResponse(
        render_block_to_string('private/space/detail/components/summary.html', 'details', {'space': space}, request))


@require_GET
def upload_events(request, space_uuid):
    space = Space.objects.get(pk=space_uuid)
    events = space.upload_events
    return render(request, 'private/space/detail/components/history_table.html', {'events': events})


@require_GET
def sender_request_files(request, space_uuid):
    space = Space.objects.get(pk=space_uuid)
    events = space.upload_events

    # Filter the events by request and sender
    events = events.filter(request__uuid=request.GET.get('request_uuid'),
                           sender__uuid=request.GET.get('sender_uuid'))

    # Get the additional parameters from the request
    hide_sender = request.GET.get('hide_sender', 'False') == 'True'
    hide_request = request.GET.get('hide_request', 'False') == 'True'

    return render(request, 'private/space/detail/components/history_table.html',
                  {'events': events, 'hide_sender': hide_sender, 'hide_request': hide_request})


@require_GET
def sender_request_modal(request, space_uuid, request_uuid, sender_uuid):
    space = get_object_or_404(Space, pk=space_uuid)
    upload_request = get_object_or_404(UploadRequest, pk=request_uuid,
                                       space=space)  # Ensures request is part of the space
    sender = get_object_or_404(Sender, pk=sender_uuid, space=space)  # Replace 'Sender' with the correct model name
    events = space.upload_events

    # Filter the events by request and sender
    events = events.filter(request__uuid=request_uuid,
                           sender__uuid=sender_uuid)

    return render(request, 'private/space/detail/components/sender_request_files_modal.html',
                  {'space': space, 'req': upload_request, 'sender': sender, 'events': events})
