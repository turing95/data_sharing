from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.http import require_POST

from utils.render_block import render_block_to_string
from web_app.models import InputRequest


@login_required
@require_POST
def request_update_order(request, request_uuid):
    kezyy_request = None
    for i, uuid in enumerate(request.POST.getlist('input_request_order[]')):
        input_request = InputRequest.objects.get(pk=uuid)
        kezyy_request = input_request.request
        input_request.position = i + 1
        input_request.save()
    html_string = render_block_to_string('private/request/detail.html', 'sorted_requests',
                                         {'kezyy_request': kezyy_request}, request)
    return HttpResponse(html_string)
