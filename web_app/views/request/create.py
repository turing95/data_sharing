from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_GET
from web_app.models import Space, Request

@login_required
@require_GET
def request_create(request, space_uuid):
    space = get_object_or_404(Space, pk=space_uuid, organization__in=request.user.organizations.all())
    space_request = Request.objects.create(space=space, title='Untitled')
    return redirect('request_detail', request_uuid=space_request.pk)
