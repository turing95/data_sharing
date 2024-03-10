from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from web_app.forms import SpaceUpdateForm
from web_app.models import Space


@login_required
@require_POST
def space_edit(request, space_uuid):
    space = get_object_or_404(Space, pk=space_uuid)
    if request.method == 'POST':
        form = SpaceUpdateForm(request.POST, instance=space)
        if form.is_valid():
            form.save()
            return HttpResponse()
    return HttpResponseBadRequest()
