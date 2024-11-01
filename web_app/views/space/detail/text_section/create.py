from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET
from web_app.models import HeadingSection, ParagraphSection, Space, SpaceSection
from django.http import HttpResponse, HttpResponseBadRequest


@login_required
@require_GET
def text_section_create(request, space_uuid):
    space = get_object_or_404(Space, pk=space_uuid)
    
    section_type = request.GET.get('section_type', 'paragraph')
    
    if section_type == 'paragraph':
        paragraph_section = ParagraphSection.objects.create(space=space) 
        space.add_section(paragraph_section=paragraph_section, prev_section_position=request.GET.get('section_position'))
    elif section_type == 'heading':
        heading_section = HeadingSection.objects.create(space=space)
        space.add_section(heading_section=heading_section, prev_section_position=request.GET.get('section_position'))
    else:
        return HttpResponseBadRequest()
        
    if request.headers.get('HX-Request'):
        response = HttpResponse()
        response['HX-Trigger'] = 'update_order'
        return response
    return redirect('space_detail', space_uuid=space.pk)

