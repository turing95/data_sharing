from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_POST
from web_app.models import CompanyField, Company


@login_required
@require_POST
def company_field_create(request, company_uuid):
    company = Company.objects.get(pk=company_uuid)
    field = CompanyField.objects.create(company=company, label='Untitled field')
    return render(request, 'private/company/detail/company_field.html',
                  {'form': field.form()})
