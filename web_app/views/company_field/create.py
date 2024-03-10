from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_POST, require_GET
from web_app.models import CompanyField, Company
from django.http import HttpResponseBadRequest
from web_app.forms import CompanyFieldForm


from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

@login_required
@require_POST
def company_field_create(request, company_uuid):
    company = get_object_or_404(Company, pk=company_uuid)
    
    label = request.POST.get('label')
    
    # Check if a CompanyField with the same label already exists for this company
    if CompanyField.objects.filter(company=company, label=label).exists():
        messages.error(request, _("A field with this label already exists for this company."))
        return render(request, 'components/messages.html', {'from_htmx': True})

    field = CompanyField.objects.create(company=company, label=label)

    return render(request, 'private/company/detail/company_field.html', {'form': field.form()})

    
    # company = Company.objects.get(pk=company_uuid)
    # field = CompanyField.objects.create(company=company, label='Untitled field')
    # return render(request, 'private/company/detail/company_field.html',
    #               {'form': field.form()})

@require_GET
@login_required
def company_field_create_modal(request, company_uuid):
    if request.method == 'GET':
        
        form = CompanyFieldForm()
        
        return render(request,
                      'private/company/detail/field_create_modal.html',
                      {'form': form,
                      'company_uuid': company_uuid})

    return HttpResponseBadRequest()