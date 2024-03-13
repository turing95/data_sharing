from django.views.decorators.http import require_POST, require_GET
from web_app.models import Company
from web_app.forms import CompanyFieldSetForm
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _


@login_required
@require_GET
def company_field_create_modal(request, company_uuid):
    if request.method == 'GET':
        company = get_object_or_404(Company, pk=company_uuid)
        form = CompanyFieldSetForm(company=company)

        return render(request,
                      'private/company/detail/field/create_update_modal.html',
                      {'form': form,
                       'company_uuid': company_uuid,
                       'confirm_button_text': _('Create field'),
                       })

    return HttpResponseBadRequest()


@login_required
@require_POST
def company_field_create(request, company_uuid):
    company = get_object_or_404(Company, pk=company_uuid)
    form = CompanyFieldSetForm(request.POST, company=company)
    if form.is_valid():
        field = form.save(commit=False)
        field.company = company
        field.save()
        response = render(request, 'private/company/detail/field/fill_form.html', {'field': field})
        response['HX-Trigger'] = 'closeModal'
        return response
    else:
        return render(request,
                      'private/company/detail/field/set_form.html',
                      {'form': form, 'from_htmx': True, 'company_uuid': company.pk,
                       'confirm_button_text': _('Create field')}
                      )
