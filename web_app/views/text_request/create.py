from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST, require_GET

from web_app.models import Request, InputRequest, TextRequest


@login_required
@require_GET
def text_request_create(request, request_uuid):
    space_request = get_object_or_404(Request, pk=request_uuid)
    text_request = TextRequest.objects.create(request=space_request)
    input_request = InputRequest.objects.create(request=space_request, text_request=text_request,position=space_request.get_new_position())
    if request.headers.get('HX-Request'):
        return render(request,
                      'private/request/input_request.html',
                      {'input_request': input_request}
                      )
    return redirect('request_detail', request_uuid=space_request.pk)
