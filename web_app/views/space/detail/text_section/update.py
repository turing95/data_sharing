from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from web_app.forms import TextRequestForm
from web_app.models import TextSection


@login_required 
@require_POST
def text_section_update(request, text_section_uuid):
    text_section = get_object_or_404(TextSection, pk=text_section_uuid)
    text_section_form = TextRequestForm(request.POST, prefix=text_section.pk, instance=text_section)
    if text_section_form.is_valid():
        text_section_form.save()
        return HttpResponse()
    return HttpResponseBadRequest()
