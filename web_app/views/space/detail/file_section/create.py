from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET
from web_app.models import FileSection, Space, SpaceSection
from django.http import HttpResponse


# @login_required
# @require_GET
# def file_section_create(request, space_uuid):
#     space = get_object_or_404(Space, pk=space_uuid)
#     file_section = FileSection.objects.create(space=space)
#     SpaceSection.objects.create(space=space,
#                                                 file_section=file_section,
#                                                 position=SpaceSection.get_new_section_position(space))

#     response = HttpResponse()
#     response['HX-Trigger'] = 'update_order'
#     return response


@login_required
@require_GET
def file_section_create(request, space_uuid):
    space = get_object_or_404(Space, pk=space_uuid)
    file_section = FileSection.objects.create(space=space)
    SpaceSection.objects.create(space=space,
                                                file_section=file_section,
                                                position=SpaceSection.get_new_section_position(space))
    
    space.add_section(file_section=file_section, prev_section_position=request.GET.get('section_position'))
    if request.headers.get('HX-Request'):
        response = HttpResponse()
        response['HX-Trigger'] = 'update_order'
        return response
    return redirect('space_detail', space_uuid=space.pk)