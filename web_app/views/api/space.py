from django.http import HttpResponse
from django.views.decorators.http import require_POST
from utils.render_block import render_block_to_string
from web_app.models import Space


@require_POST
def toggle_space_active(request, space_uuid):
    space = Space.objects.get(pk=space_uuid)
    space.is_active = not space.is_active
    space.save()
    return HttpResponse(render_block_to_string('private/space/detail/components/summary.html', 'details', {'space': space},request))

@require_POST
def toggle_space_public(request, space_uuid):
    space = Space.objects.get(pk=space_uuid)
    space.is_public = not space.is_public
    space.save()
    return HttpResponse(render_block_to_string('private/space/detail/components/summary.html', 'details', {'space': space},request))
