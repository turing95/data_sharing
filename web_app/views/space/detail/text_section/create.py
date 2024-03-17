from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET
from web_app.models import TextSection, Space, SpaceSection
from django.http import HttpResponse


@login_required
@require_GET
def text_section_create(request, space_uuid):
    space = get_object_or_404(Space, pk=space_uuid)
    text_section = TextSection.objects.create(space=space)
                    
    
    space.add_section(text_section=text_section, prev_section_position=request.GET.get('section_position'))
    if request.headers.get('HX-Request'):
        response = HttpResponse()
        response['HX-Trigger'] = 'update_order'
        return response
    return redirect('space_detail', space_uuid=space.pk)