from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from utils.render_block import render_block_to_string
from web_app.forms.widgets import ToggleWidget
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
@require_POST
def input_request_update_active(request, input_request_uuid):
    if request.method == 'POST':
        input_request = get_object_or_404(InputRequest, pk=input_request_uuid)
        if input_request.upload_request:
            if input_request.upload_request.active_destination:
                input_request.is_active = not input_request.is_active
                input_request.save()
        elif input_request.text_request:
            input_request.is_active = not input_request.is_active
            input_request.save()
        return render(request,'forms/widgets/toggle.html', ToggleWidget().get_context('input_request_active_toggle', input_request.is_active,
                                              {'hx-post': reverse('input_request_update_active',
                                                                  kwargs={'input_request_uuid': input_request.pk}),
                                               'hx-trigger': "click", 'hx-swap': 'outerHTML','hx-target':'closest .toggle-container'}))
    return HttpResponseBadRequest()


@login_required
@require_POST
def input_request_update_complete(request, input_request_uuid):
    if request.method == 'POST':
        input_request = get_object_or_404(InputRequest, pk=input_request_uuid)
        input_request.is_complete = not input_request.is_complete
        input_request.save()
        return HttpResponse()
    return HttpResponseBadRequest()
