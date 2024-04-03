from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from web_app.models import TextField, FieldGroup
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@require_POST
@login_required
def text_field_delete(request, field_uuid):
    field = get_object_or_404(TextField, pk=field_uuid)
    field.delete()

    response = HttpResponse()
    response['HX-Trigger'] = f'{field.group.update_event}'
    return response


@require_POST
@login_required
def field_group_delete(request, group_uuid):
    group = get_object_or_404(FieldGroup, pk=group_uuid)
    group.delete()
    response = HttpResponse()
    response['HX-Trigger'] = f'{group.group.update_event}'
    return response
