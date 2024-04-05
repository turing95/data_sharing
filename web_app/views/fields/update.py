from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.views.decorators.http import require_POST, require_GET
from web_app.models import TextField, FieldGroup, FieldGroupTemplate, FileField, File, GenericDestination, Kezyy, \
    FileFileField
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse


@login_required
@require_POST
def text_field_update(request, field_uuid):
    text_field = get_object_or_404(TextField, pk=field_uuid)
    form = text_field.set_form(request.POST)
    if form.is_valid():
        form.save()
        response = HttpResponse(status=204)
        response['HX-Trigger'] = f"{text_field.group.update_event}, closeModal"
        return response
    return render(request,
                  'private/company/detail/field/text_set_form.html',
                  {'form': form, 'field': text_field, 'confirm_button_text': _('Update field')}
                  )


@login_required
@require_POST
def file_field_update(request, field_uuid):
    file_field = get_object_or_404(FileField, pk=field_uuid)
    form = file_field.set_form(request.POST)
    if form.is_valid():
        form.save()
        response = HttpResponse(status=204)
        response['HX-Trigger'] = f"{file_field.group.update_event}, closeModal"
        return response
    return render(request,
                  'private/company/detail/field/file_set_form.html',
                  {'form': form,
                   'field': file_field,
                   'confirm_button_text': _('Update field')}
                  )


@login_required
@require_POST
def field_group_update(request, group_uuid):
    group = get_object_or_404(FieldGroup, pk=group_uuid)
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
def text_field_update_value(request, field_uuid):
    text_field = get_object_or_404(TextField, pk=field_uuid)
    form = text_field.form(request.POST)
    if form.is_valid():
        form.save()
        response = HttpResponse(status=204)
        response['HX-Trigger'] = text_field.group.update_event  # togliere questo per aggionare solo field
        return response
    return HttpResponseBadRequest()


@login_required
@require_POST
def file_field_update_value(request, field_uuid):
    file_field = get_object_or_404(FileField, pk=field_uuid)
    form = file_field.form(request.POST, request.FILES)
    if form.is_valid():
        uploaded_files = form.cleaned_data.pop('files')
        for uploaded_file in uploaded_files:
            kezyy_destination = GenericDestination.create_provider(Kezyy.TAG)
            file_url = kezyy_destination.upload_file(uploaded_file,
                                                     uploaded_file.name)
            file = File.objects.create(original_name=uploaded_file.name,
                                       size=uploaded_file.size,
                                       file_type=uploaded_file.content_type,
                                       destination=kezyy_destination,
                                       uid=file_url)
            FileFileField.objects.create(file=file, field=file_field)

            response = HttpResponse(status=204)
            response['HX-Trigger'] = file_field.group.update_event
            return response
    return HttpResponseBadRequest()


@login_required
@require_GET
def text_field_update_modal(request, field_uuid):
    field = get_object_or_404(TextField, pk=field_uuid)
    form = field.set_form()
    return render(request,
                  'private/company/detail/field/create_update_modal.html',
                  {'form': form,
                   'text_field': True,
                   'field': field,
                   'confirm_button_text': _('Update field'),
                   })


@login_required
@require_GET
def file_field_update_modal(request, field_uuid):
    field = get_object_or_404(FileField, pk=field_uuid)
    form = field.set_form()
    return render(request,
                  'private/company/detail/field/create_update_modal.html',
                  {'form': form,
                   'file_field': True,
                   'field': field,
                   'confirm_button_text': _('Update field'),
                   })


@login_required
@require_GET
def field_group_update_modal(request, group_uuid):
    group = get_object_or_404(FieldGroup, pk=group_uuid)
    form = group.set_form()
    return render(request,
                  'private/company/detail/group/create_update_modal.html',
                  {'form': form,
                   'group': group,
                   'confirm_button_text': _('Update group'),
                   'heading': _('Update group of fields')
                   })


@login_required
@require_POST
def field_group_add_template(request, group_uuid, template_uuid):
    group = get_object_or_404(FieldGroup, pk=group_uuid)
    template = get_object_or_404(FieldGroupTemplate, pk=template_uuid)
    group.add_template(template)
    response = HttpResponse(status=204)
    response['HX-Trigger'] = f"{group.update_event}"
    return response
