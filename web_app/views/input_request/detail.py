from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.http import require_GET

from utils.render_block import render_block_to_string
from web_app.models import UploadRequest, InputRequest


@login_required
@require_GET
def input_request_detail_show(request, input_request_uuid):
    if request.method == 'GET':
        input_request = InputRequest.objects.get(pk=input_request_uuid)
        if input_request.upload_request:
            upload_request = input_request.upload_request
            show_more = request.GET.get('show_more', False)

            return render(request, 'private/request/upload_request_detail.html',
                          {'upload_request': upload_request, 'show_more': show_more, 'from_htmx': True})
        elif input_request.text_request:
            text_request = input_request.text_request
            show_more = request.GET.get('show_more', False)

            return render(request, 'private/request/text_request_detail.html',
                          {'text_request': text_request, 'show_more': show_more, 'from_htmx': True})
    return HttpResponseBadRequest()

