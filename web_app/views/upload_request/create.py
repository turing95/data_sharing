from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST, require_GET
from django.http import HttpResponse

from web_app.models import Request, UploadRequest, GenericDestination, Kezyy, InputRequest



@login_required
@require_GET
def upload_request_create(request, request_uuid):
    space_request = get_object_or_404(Request, pk=request_uuid)
    upload_request = UploadRequest.objects.create(request=space_request,title='Untitled')
    space_request.add_input_request(upload_request=upload_request,
                                                    prev_request_position=request.GET.get('input_request_position'))
    if request.headers.get('HX-Request'):
        response = HttpResponse()
        response['HX-Trigger'] = 'update_order'
        return response
    return redirect('request_detail', request_uuid=space_request.pk)