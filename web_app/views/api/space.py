from django.shortcuts import render
from django.views.decorators.http import require_POST

from web_app.models import Space


@require_POST
def toggle_space_active(request, space_uuid):
    space = Space.objects.get(pk=space_uuid)
    space.is_active = not space.is_active
    space.save()
    return render(
        request,
        'components/space/status.html',
        {'space': space}
    )
