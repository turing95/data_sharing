from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_POST
from web_app.models import UploadRequest

@login_required
@require_POST
def delete_request(request, request_uuid):
    req = UploadRequest.objects.get(pk=request_uuid)
    space = req.space
    req.delete()
    space.refresh_from_db()
    return render(
        request,
        'private/space/create/components/request_form.html',
        {'action': 'edit'}
    )
