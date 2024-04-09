from django.http import HttpResponse
from django.views.decorators.http import require_POST, require_GET
from web_app.models import TextField, FieldGroup, GroupElement, FileField
from web_app.forms import TextFieldSetForm, FieldGroupSetForm, FileFieldSetForm
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _


@login_required
@require_GET
def text_field_create_modal(request, group_uuid):
    group = get_object_or_404(FieldGroup, pk=group_uuid)
    form = TextFieldSetForm(group=group)

    return render(request,
                  'private/company/detail/field/create_update_modal.html',
                  {'form': form,
                   'text_field': True,
                   'group_uuid': group_uuid,
                   'confirm_button_text': _('Create field'),
                   })


@login_required
@require_GET
def file_field_create_modal(request, group_uuid):
    group = get_object_or_404(FieldGroup, pk=group_uuid)
    form = FileFieldSetForm(group=group)

    return render(request,
                  'private/company/detail/field/create_update_modal.html',
                  {'form': form,
                   'file_field': True,
                   'group_uuid': group_uuid,
                   'confirm_button_text': _('Create field'),
                   })


@login_required
@require_GET
def field_group_create_modal(request, group_uuid):
    group = get_object_or_404(FieldGroup, pk=group_uuid)
    form = FieldGroupSetForm(group=group)

    return render(request,
                  'private/company/detail/group/create_update_modal.html',
                  {'form': form,
                   'group_uuid': group_uuid,
                   'confirm_button_text': _('Create group'),
                   'heading': _('Create a new group of fields'),
                   })


@login_required
@require_POST
def text_field_create(request, group_uuid):
    group = get_object_or_404(FieldGroup, pk=group_uuid)
    form = TextFieldSetForm(request.POST, group=group)
    if form.is_valid():
        field = form.save(commit=False)
        field.group = group
        field.organization = group.organization
        field.save()
        GroupElement.objects.create(parent_group=group, text_field=field,
                                    position=group.children_elements.count() + 1)
        response = HttpResponse()
        response['HX-Trigger'] = f'{group.update_event},closeModal'
        return response
    else:
        return render(request,
                      'private/company/detail/field/text_set_form.html',
                      {'form': form, 'from_htmx': True, 'group_uuid': group.pk,
                       'confirm_button_text': _('Create field')}
                      )


@login_required
@require_POST
def file_field_create(request, group_uuid):
    group = get_object_or_404(FieldGroup, pk=group_uuid)
    form = FileFieldSetForm(request.POST, group=group)
    if form.is_valid():
        field = form.save(commit=False)
        field.group = group
        field.organization = group.organization
        field.save()
        GroupElement.objects.create(parent_group=group, file_field=field,
                                    position=group.children_elements.count() + 1)
        response = HttpResponse()
        response['HX-Trigger'] = f'{group.update_event},closeModal'
        return response
    else:
        return render(request,
                      'private/company/detail/field/file_set_form.html',
                      {'form': form, 'from_htmx': True, 'group_uuid': group.pk,
                       'confirm_button_text': _('Create field')}
                      )


@login_required
@require_POST
def field_group_create(request, group_uuid):
    group = get_object_or_404(FieldGroup, pk=group_uuid)
    form = FieldGroupSetForm(request.POST, group=group)
    if form.is_valid():
        new_group = form.save(commit=False)
        new_group.group = group
        new_group.company = group.company
        new_group.organization = group.organization
        new_group.save()
        GroupElement.objects.create(parent_group=group, group=new_group,
                                    position=group.children_elements.count() + 1)
        response = HttpResponse()
        response['HX-Trigger'] = f'{group.update_event},closeModal'
        return response
    else:
        return render(request,
                      'private/company/detail/group/set_form.html',
                      {'form': form, 'from_htmx': True, 'group_uuid': group.pk,
                       'confirm_button_text': _('Create group'),
                       }
                      )


@login_required
@require_GET
def text_field_duplicate(request, field_uuid):
    field = get_object_or_404(TextField, pk=field_uuid)
    new_field = field.duplicate()
    GroupElement.objects.create(parent_group=new_field.group, text_field=new_field,
                                position=new_field.group.children_elements.count() + 1)
    response = HttpResponse()
    response['HX-Trigger'] = new_field.group.update_event
    return response


@login_required
@require_POST
def text_field_to_template(request, text_field_uuid):
    text_field = get_object_or_404(TextField, pk=text_field_uuid)
    text_field.to_template()
    return HttpResponse(status=204)


@login_required
@require_GET
def file_field_duplicate(request, field_uuid):
    field = get_object_or_404(FileField, pk=field_uuid)
    new_field = field.duplicate()
    GroupElement.objects.create(parent_group=new_field.group, file_field=new_field,
                                position=new_field.group.children_elements.count() + 1)
    response = HttpResponse()
    response['HX-Trigger'] = new_field.group.update_event
    return response


@login_required
@require_POST
def file_field_to_template(request, file_field_uuid):
    file_field = get_object_or_404(FileField, pk=file_field_uuid)
    file_field.to_template()
    return HttpResponse(status=204)


@login_required
@require_GET
def field_group_duplicate(request, group_uuid):
    group = get_object_or_404(FieldGroup, pk=group_uuid)
    new_group = group.duplicate()
    GroupElement.objects.create(parent_group=new_group.group, group=new_group,
                                position=new_group.group.children_elements.count() + 1)
    response = HttpResponse()
    response['HX-Trigger'] = new_group.group.update_event
    return response


@login_required
@require_POST
def field_group_to_template(request, group_uuid):
    group = get_object_or_404(FieldGroup, pk=group_uuid)
    group.to_template()
    return HttpResponse(status=204)
