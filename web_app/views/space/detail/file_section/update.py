from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from web_app.forms import FileSectionForm
from web_app.models import FileSection


@login_required
@require_POST
def file_section_update(request, file_section_uuid):
    file_section = get_object_or_404(FileSection, pk=file_section_uuid)
    file_section_form = FileSectionForm(request.POST, prefix=file_section.pk, instance=file_section)
    if file_section_form.is_valid():
        file_section_form.save()
        return HttpResponse()
    return HttpResponseBadRequest()
