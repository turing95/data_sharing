from django.http import HttpResponse
from django.views.decorators.http import require_POST, require_GET
from web_app.models import CompanyField, CompanyFieldGroup, CompanyGroupElement
from web_app.forms import CompanyFieldSetForm, CompanyFieldGroupSetForm
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _


@login_required
@require_GET
def company_field_create_modal(request, group_uuid):
    group = get_object_or_404(CompanyFieldGroup, pk=group_uuid)
    form = CompanyFieldSetForm(group=group)

    return render(request,
                  'private/company/detail/field/create_update_modal.html',
                  {'form': form,
                   'group_uuid': group_uuid,
                   'confirm_button_text': _('Create field'),
                   })


@login_required
@require_GET
def company_field_group_create_modal(request, group_uuid):
    group = get_object_or_404(CompanyFieldGroup, pk=group_uuid)
    form = CompanyFieldGroupSetForm(group=group)

    return render(request,
                  'private/company/detail/group/create_update_modal.html',
                  {'form': form,
                   'group_uuid': group_uuid,
                   'confirm_button_text': _('Create group'),
                   })


@login_required
@require_POST
def company_field_create(request, group_uuid):
    group = get_object_or_404(CompanyFieldGroup, pk=group_uuid)
    form = CompanyFieldSetForm(request.POST, group=group)
    if form.is_valid():
        field = form.save(commit=False)
        field.group = group
        field.organization = group.organization
        field.save()
        CompanyGroupElement.objects.create(parent_group=group, field=field,
                                           position=group.children_elements.count() + 1)
        response = HttpResponse()
        response['HX-Trigger'] = f'{group.update_event},closeModal'
        return response
    else:
        return render(request,
                      'private/company/detail/field/set_form.html',
                      {'form': form, 'from_htmx': True, 'group_uuid': group.pk,
                       'confirm_button_text': _('Create field')}
                      )


@login_required
@require_POST
def company_field_group_create(request, group_uuid):
    group = get_object_or_404(CompanyFieldGroup, pk=group_uuid)
    form = CompanyFieldGroupSetForm(request.POST, group=group)
    if form.is_valid():
        new_group = form.save(commit=False)
        new_group.group = group
        new_group.organization = group.organization
        new_group.save()
        CompanyGroupElement.objects.create(parent_group=group, group=new_group,
                                           position=group.children_elements.count() + 1)
        response = HttpResponse()
        response['HX-Trigger'] = f'{group.update_event},closeModal'
        return response
    else:
        return render(request,
                      'private/company/detail/group/set_form.html',
                      {'form': form, 'from_htmx': True, 'group_uuid': group.pk,
                       'confirm_button_text': _('Create group')}
                      )


@login_required
@require_GET
def company_field_duplicate(request, company_field_uuid):
    field = get_object_or_404(CompanyField, pk=company_field_uuid)
    new_field = field.duplicate()
    CompanyGroupElement.objects.create(parent_group=new_field.group, field=new_field,
                                       position=new_field.group.children_elements.count() + 1)
    response = HttpResponse()
    response['HX-Trigger'] = new_field.group.update_event
    return response


@login_required
@require_POST
def company_field_to_template(request, company_field_uuid):
    field = get_object_or_404(CompanyField, pk=company_field_uuid)
    field.to_template()
    return HttpResponse(status=204)


@login_required
@require_POST
def company_field_group_to_template(request, group_uuid):
    group = get_object_or_404(CompanyFieldGroup, pk=group_uuid)
    group.to_template()
    return HttpResponse(status=204)
