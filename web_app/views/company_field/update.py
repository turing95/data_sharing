from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.http import require_POST, require_GET
from web_app.models import CompanyField
from django.utils.translation import gettext_lazy as _
from web_app.forms import CompanyFieldSetForm
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
import json
from django.http import HttpResponse

@login_required
@require_POST
def company_field_update(request, company_field_uuid):
        company_field = get_object_or_404(CompanyField, pk=company_field_uuid)
        form = CompanyFieldSetForm(request.POST, instance=company_field, company=company_field.company)
        if form.is_valid():
            form.save()
            messages.success(request, _('Field updated successfully'))
            response = HttpResponse(status=204)
            response['HX-Trigger'] = f"closeModal, {company_field.update_event}"
            return response

        return render(request,
                'private/company/detail/field/set_form.html',
                {'form': form, 'field': company_field, 'confirm_button_text': _('Update field'), 'from_htmx': True}
                )


@login_required
@require_GET
def company_field_fill_form_refresh(request, company_field_uuid):
        company_field = get_object_or_404(CompanyField,pk=company_field_uuid)
   
        return render(request,
                'private/company/detail/field/fill_form.html',
                {'field': company_field,
                 'from_htmx': True}
                )




@login_required
@require_POST
def company_field_update_value(request, company_field_uuid):
        company_field = get_object_or_404(CompanyField,pk=company_field_uuid)
        form = company_field.form(request.POST)
        if form.is_valid():
            form.save()  
            response = HttpResponse(status=204)
            response['HX-Trigger'] = company_field.update_event
            return response
        else:
            return HttpResponse(status=400)




@login_required
@require_GET
def company_field_update_modal(request, company_field_uuid):
    if request.method == 'GET':
        field = get_object_or_404(CompanyField, pk=company_field_uuid)
        form = CompanyFieldSetForm(instance=field, company=field.company)

        return render(request,
                      'private/company/detail/field/create_update_modal.html',
                      {'form': form,
                       'field': field,
                       'confirm_button_text': _('Update field'),
                       })

    return HttpResponseBadRequest()
