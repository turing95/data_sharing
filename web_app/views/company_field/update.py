from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.http import require_POST, require_GET
from web_app.models import CompanyField, CompanyFieldGroup, CompanyTemplate
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
    form = company_field.set_form(request.POST)
    if form.is_valid():
        form.save()
        response = HttpResponse(status=204)
        response['HX-Trigger'] = f"{company_field.update_event}, closeModal"
        return response
    return render(request,
                  'private/company/detail/field/set_form.html',
                  {'form': form, 'field': company_field, 'confirm_button_text': _('Update field')}
                  )


@login_required
@require_POST
def company_field_group_update(request, group_uuid):
    group = get_object_or_404(CompanyFieldGroup, pk=group_uuid)
    form = group.set_form(request.POST)
    if form.is_valid():
        form.save()
        response = HttpResponse(status=204)
        response['HX-Trigger'] = f"{group.update_event}, closeModal"
        return response
    return render(request,
                  'private/company/detail/group/set_form.html',
                  {'form': form, 'group': group, 'confirm_button_text': _('Update field')}
                  )


@login_required
@require_POST
def company_field_update_value(request, company_field_uuid):
    company_field = get_object_or_404(CompanyField, pk=company_field_uuid)
    form = company_field.form(request.POST)
    if form.is_valid():
        form.save()
        response = HttpResponse(status=204)
        response['HX-Trigger'] = company_field.update_event
        return response
    return HttpResponseBadRequest()


@login_required
@require_GET
def company_field_update_modal(request, company_field_uuid):
    field = get_object_or_404(CompanyField, pk=company_field_uuid)
    form = field.set_form()
    return render(request,
                  'private/company/detail/field/create_update_modal.html',
                  {'form': form,
                   'field': field,
                   'confirm_button_text': _('Update field'),
                   })


@login_required
@require_GET
def company_field_group_update_modal(request, group_uuid):
    group = get_object_or_404(CompanyFieldGroup, pk=group_uuid)
    form = group.set_form()
    return render(request,
                  'private/company/detail/group/create_update_modal.html',
                  {'form': form,
                   'group': group,
                   'confirm_button_text': _('Update group'),
                   })


@login_required
@require_POST
def company_field_group_add_template(request, group_uuid, template_uuid):
    group = get_object_or_404(CompanyFieldGroup, pk=group_uuid)
    template = get_object_or_404(CompanyTemplate, pk=template_uuid)
    group.add_template(template)
    response = HttpResponse(status=204)
    response['HX-Trigger'] = f"{group.update_event}"
    return response
