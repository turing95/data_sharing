from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST, require_GET
from utils.render_block import render_block_to_string
from web_app.models import Space


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


# @require_GET
# def upload_events(request, space_uuid):
#     space = Space.objects.get(pk=space_uuid)
#     return render(request, 'private/space/detail/components/history_table.html', {'space': space})

@require_GET
def upload_events(request, space_uuid, sender_uuid=None, request_uuid=None):
    space = Space.objects.get(pk=space_uuid)
    events = space.get_filtered_upload_events(request_uuid=request_uuid, sender_uuid=sender_uuid)
    
        # Get the additional parameters from the request
    hide_sender = request.GET.get('hide_sender', False) 
    hide_request = request.GET.get('hide_request', False) 

    return render(request, 'private/space/detail/components/history_table.html',
                  {'events': events, 'hide_sender': hide_sender, 'hide_request': hide_request})

