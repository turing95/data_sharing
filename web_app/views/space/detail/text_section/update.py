from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from web_app.forms import ParagraphSectionForm,HeadingSectionForm
from web_app.models import ParagraphSection, HeadingSection


@login_required 
@require_POST
def text_section_update(request, section_uuid):
    
    section_type = request.GET.get('section_type', 'paragraph')    
    if section_type == 'paragraph':
        paragraph_section = get_object_or_404(ParagraphSection, pk=section_uuid)
        section_form = ParagraphSectionForm(request.POST, prefix=paragraph_section.pk, instance=paragraph_section)
    elif section_type == 'heading':
        heading_section = get_object_or_404(HeadingSection, pk=section_uuid)
        section_form = HeadingSectionForm(request.POST, prefix=heading_section.pk, instance=heading_section)
    else:
        return HttpResponseBadRequest()
    
    if section_form.is_valid():
        section_form.save()
        return HttpResponse()
    return HttpResponseBadRequest()
