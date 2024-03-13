from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET
from web_app.models import TextSection, Space, SpaceSection


@login_required
@require_GET
def text_section_create(request, space_uuid):
    space = get_object_or_404(Space, pk=space_uuid)
    text_section = TextSection.objects.create(space=space)
    space_section = SpaceSection.objects.create(space=space,
                                                text_section=text_section,
                                                position=SpaceSection.get_new_section_position(space))

    if request.headers.get('HX-Request'):
        return render(request,
                      'private/space/detail/content/space_section.html',
                      {'space_section': space_section,
                       'space': space}
                      )
    return redirect('space_detail', space_uuid=space.pk)
