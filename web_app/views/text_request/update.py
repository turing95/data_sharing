from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST, require_GET
from web_app.models import TextRequest


@login_required
@require_POST
def text_request_update(request, text_request_uuid):
    text_request = get_object_or_404(TextRequest, pk=text_request_uuid)
    text_request_form = text_request.request_form(request.POST)
    if text_request_form.is_valid():
        text_request_form.save()
    return render(request, 'private/request/edit/text_request_detail.html', {
        'text_request': text_request, 'show_more': True, 'form': text_request_form
    })
