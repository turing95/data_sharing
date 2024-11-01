from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from web_app.models import SpaceSection
from django.http import HttpResponse


@login_required
@require_POST
def section_delete(request, space_section_uuid):
    section = get_object_or_404(SpaceSection, pk=space_section_uuid)
    section.delete()  
    response = HttpResponse()
    response['HX-Trigger'] = 'update_order'
    return response