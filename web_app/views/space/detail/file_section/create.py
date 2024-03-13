from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET
from web_app.models import FileSection, Space, SpaceSection


@login_required
@require_GET
def file_section_create(request, space_uuid):
    space = get_object_or_404(Space, pk=space_uuid)
    file_section = FileSection.objects.create(space=space)
    space_section = SpaceSection.objects.create(space=space,
                                                file_section=file_section,
                                                position=SpaceSection.get_new_section_position(space))

    if request.headers.get('HX-Request'):
        return render(request,
                      'private/space/detail/content/space_section.html',
                      {'space_section': space_section,
                       'space': space}
                      )
    return redirect('space_detail', space_uuid=space.pk)
