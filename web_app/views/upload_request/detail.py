from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from utils.render_block import render_block_to_string
from web_app.models import UploadRequest


@login_required
@require_GET
def upload_request_detail_show(request, upload_request_uuid):
    upload_request = UploadRequest.objects.get(pk=upload_request_uuid)
    show_more = request.GET.get('show_more', False)

    return render(request, 'private/request/upload_request_detail.html',
                  {'upload_request': upload_request, 'show_more': show_more, 'from_htmx': True})
