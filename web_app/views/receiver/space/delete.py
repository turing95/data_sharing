from django.shortcuts import get_object_or_404, redirect
from web_app.models import Space
from django.contrib.auth.decorators import login_required


@login_required
def delete_space(request, space_uuid):
    space = get_object_or_404(Space, uuid=space_uuid)
    space.delete()
    return redirect('spaces')
