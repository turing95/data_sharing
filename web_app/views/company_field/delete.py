from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from web_app.models import CompanyField
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@require_POST
@login_required
def company_field_delete(request, company_field_uuid):
    field = get_object_or_404(CompanyField, pk=company_field_uuid)
    field.delete()
    return HttpResponse('')
