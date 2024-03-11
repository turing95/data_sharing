from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from web_app.forms import FileSectionForm
from web_app.models import FileSection, GenericDestination, File


@login_required
@require_POST
def file_section_update(request, file_section_uuid):
    file_section = get_object_or_404(FileSection, pk=file_section_uuid)
    print(request.POST)
    print(request.FILES)
    file_section_form = FileSectionForm(request.POST, request.FILES, prefix=file_section.pk, instance=file_section)
    if file_section_form.is_valid():
        uploaded_file = file_section_form.cleaned_data.pop('file')
        file_section_form.save()
        print(file_section_form.cleaned_data)
        if uploaded_file:
            kezyy_destination = file_section.space.destinations.first()
            if kezyy_destination:
                file_url = kezyy_destination.upload_file(uploaded_file,
                                                         uploaded_file.name)
                file = File.objects.create(original_name=uploaded_file.name,
                                           size=uploaded_file.size,
                                           file_type=uploaded_file.content_type,
                                           destination=kezyy_destination,
                                           uid=file_url,
                                           company=file_section.space.company)
                file_section.file = file
                file_section.save()
        return HttpResponse()
    return HttpResponseBadRequest()
