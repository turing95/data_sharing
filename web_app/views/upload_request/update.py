from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST, require_GET
from web_app.forms import UploadRequestForm
from web_app.models import Request, UploadRequest, GenericDestination, Kezyy, InputRequest


def handle_destination(request, form):
    if form.instance.destination:
        if form.instance.destination.folder_id == form.cleaned_data.get('destination_id'):
            if form.instance.destination.is_active is False:
                # if inactive and same, create new
                GenericDestination.create_from_form(request, form)
        else:
            # If the folder ID doesn't match, create a new destination.
            GenericDestination.create_from_form(request, form)

    else:
        # If no current destination exists, create a new one.
        GenericDestination.create_from_form(request, form)

    # Activate the instance in all cases after handling the destination.
    form.instance.is_active = True
    form.instance.save()


@login_required
@require_POST 
def upload_request_update(request, upload_request_uuid):
    if request.method == 'POST':
        upload_request = get_object_or_404(UploadRequest, pk=upload_request_uuid)
        upload_request_form = UploadRequestForm(request.POST, prefix=upload_request.pk, instance=upload_request,
                                                user=request.user)
        if upload_request_form.is_valid():
            upload_request_form.save()
            if upload_request_form.cleaned_data.get('destination_type'):
                handle_destination(request, upload_request_form)
            return HttpResponse()
    return HttpResponseBadRequest()


@login_required
@require_POST
def upload_request_update_active(request, upload_request_uuid):
    if request.method == 'POST':
        upload_request = get_object_or_404(UploadRequest, pk=upload_request_uuid)
        upload_request.is_active = not upload_request.is_active
        upload_request.save()
        return HttpResponse()
    return HttpResponseBadRequest()
