from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.http import require_GET

from utils.render_block import render_block_to_string
from web_app.models import UploadRequest


@login_required
@require_GET
def upload_request_detail_show(request, upload_request_uuid):
    upload_request = UploadRequest.objects.get(pk=upload_request_uuid)
    show_more = request.GET.get('show_more', False)
    html_string = render_block_to_string('private/request/upload_request.html', 'upload_request_detail',
                                         {'upload_request': upload_request, 'show_more': show_more}, request)
    return HttpResponse(html_string)
