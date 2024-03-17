from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST, require_GET
from utils.render_block import render_block_to_string
from web_app.models import InputRequest, Request


@login_required
@require_POST
def request_update_order(request, request_uuid):
    kezyy_request = get_object_or_404(Request, pk=request_uuid)
    for i, uuid in enumerate(request.POST.getlist('input_request_order[]')):
        input_request = InputRequest.objects.get(pk=uuid)
        input_request.position = i + 1
        input_request.save()

    html_string = render_block_to_string('private/request/edit.html', 'sorted_requests',
                                         {'kezyy_request': kezyy_request}, request)
    return HttpResponse(html_string)


@login_required
@require_GET
def input_requests(request, request_uuid):
    kezyy_request = get_object_or_404(Request, pk=request_uuid)

    html_string = render_block_to_string('private/request/edit.html', 'sorted_requests',
                                         {'kezyy_request': kezyy_request}, request)
    return HttpResponse(html_string)
