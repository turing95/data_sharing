from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from web_app.models import Request, InputRequest, TextRequest
from django.http import HttpResponse

@login_required
@require_POST
def input_request_delete(request, input_request_uuid):
    input_request = get_object_or_404(InputRequest, pk=input_request_uuid)
    input_request.delete()  
    response = HttpResponse()
    response['HX-Trigger'] = 'update_order'
    return response