from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET
from web_app.models import Request, InputRequest, TextRequest


@login_required
@require_GET
def text_request_create(request, request_uuid):
    space_request = get_object_or_404(Request, pk=request_uuid)
    text_request = TextRequest.objects.create(request=space_request)
    input_request = space_request.add_input_request(space_request, specific_input_request=text_request,
                                                prev_request_position=request.GET.get('input_request_position'))

    if request.headers.get('HX-Request'):
        return render(request,
                      'private/request/input_request.html',
                      {'input_request': input_request,
                       'data_position': input_request.position,
                       'kezyy_request': space_request}
                      )
    return redirect('request_detail', request_uuid=space_request.pk)
