from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET
from web_app.models import Request, InputRequest, TextRequest
from django.http import HttpResponse

@login_required
@require_GET
def text_request_create(request, request_uuid):
    space_request = get_object_or_404(Request, pk=request_uuid)
    text_request = TextRequest.objects.create(request=space_request,title='Untitled')
    space_request.add_input_request(text_request=text_request,
                                                prev_request_position=request.GET.get('input_request_position'))

    if request.headers.get('HX-Request'):
        response = HttpResponse()
        response['HX-Trigger'] = 'update_order'
        return response

    return redirect('request_detail', request_uuid=space_request.pk)
