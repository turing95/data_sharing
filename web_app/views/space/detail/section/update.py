from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST, require_GET

from utils.render_block import render_block_to_string
from web_app.models import SpaceSection, Space


@login_required
@require_POST
def space_section_update_order(request, space_uuid):
    space = get_object_or_404(Space, pk=space_uuid)
    for i, uuid in enumerate(request.POST.getlist('space_section_order[]')):
        space_section = SpaceSection.objects.get(pk=uuid)
        space_section.position = i + 1
        space_section.save()
    html_string = render_block_to_string("private/space/detail/base.html", 'sorted_sections',
                                         {'space': space}, request)
    return HttpResponse(html_string)


@login_required
@require_GET
def sections(request, space_uuid):
    space = get_object_or_404(Space, pk=space_uuid)
    html_string = render_block_to_string("private/space/detail/base.html", 'sorted_sections',
                                         {'space': space}, request)
    return HttpResponse(html_string)
