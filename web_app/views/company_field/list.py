from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET

from web_app.models import Company, CompanyFieldGroup


@login_required
@require_GET
def company_field_list(request, company_uuid):
    company = get_object_or_404(Company, pk=company_uuid)
    company_fields = company.fields.all()
    return render(request,
                  'private/company/detail/field/list.html',
                  {'company': company,
                   'company_fields': company_fields}
                  )


@login_required
@require_GET
def group_elements(request, group_uuid):
    group = get_object_or_404(CompanyFieldGroup, pk=group_uuid)
    if request.GET.get('template'):
        return render(request,
                      'private/company_templates/detail/group/elements.html',
                      {'group': group}
                      )
    else:
        return render(request,
                      'private/company/detail/group/elements.html',
                      {'group': group}
                      )
