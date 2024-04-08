from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from web_app.models import File, Output, Sender, FileFileField


@require_POST
@login_required
def accept(request, output_uuid):
    output = get_object_or_404(Output, pk=output_uuid)
    output.status = Output.OutputStatus.ACCEPTED
    output.save()
    if output.sender_event.text_request:
        text_request = output.sender_event.text_request
        if text_request.target:
            target = text_request.target
            target.value = output.content
            target.save()
    elif output.sender_event.upload_request:
        upload_request = output.sender_event.upload_request
        if upload_request.target:
            FileFileField.objects.create(field=upload_request.target, file=output.file)
    response = HttpResponse()
    response['HX-Trigger'] = output.update_event
    return response


@require_POST
@login_required
def reject(request, output_uuid):
    output = get_object_or_404(Output, pk=output_uuid)
    reject_form = output.reject_form(request.POST)
    if reject_form.is_valid():
        output.status = Output.OutputStatus.REJECTED
        output.feedback = reject_form.save()
        output.save()
        response = HttpResponse()
        response['HX-Trigger'] = f'{output.update_event}, closeModal'
        return response
    return HttpResponseBadRequest()
