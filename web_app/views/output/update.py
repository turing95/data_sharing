from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from web_app.models import File, Output, Sender


@require_POST
@login_required
def accept(request, output_uuid):
    output = get_object_or_404(Output, pk=output_uuid)
    output.status = Output.OutputStatus.ACCEPTED
    output.save()
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
