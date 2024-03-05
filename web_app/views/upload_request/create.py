from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST, require_GET

from web_app.models import Request, UploadRequest, GenericDestination, Kezyy, InputRequest


@login_required
@require_GET
def upload_request_create(request, request_uuid):
    space_request = get_object_or_404(Request, pk=request_uuid)
    upload_request = UploadRequest.objects.create(request=space_request)
    input_request = InputRequest.objects.create(request=space_request, upload_request=upload_request)
    GenericDestination.create_provider(upload_request, Kezyy.TAG, request.user)
    if request.headers.get('HX-Request'):
        return render(request,
                      'private/request/input_request.html',
                      {'input_request': input_request}
                      )
    return redirect('request_detail', request_uuid=space_request.pk)