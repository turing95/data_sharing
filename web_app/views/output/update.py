from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from web_app.models import File, Output, Sender
from django.http import HttpResponseBadRequest
from django.utils.translation import gettext_lazy as _


@require_POST
@login_required
def accept(request, output_uuid):
    if request.method == 'POST':
        output = get_object_or_404(Output, pk=output_uuid)
        output.status = Output.OutputStatus.ACCEPTED
        output.save()
        messages.success(request, _('Accepted'))
        return render(
            request,
            'components/messages.html',
            {'from_htmx': True}
        )
    return HttpResponseBadRequest()


@require_POST
@login_required
def reject(request, output_uuid):
    if request.method == 'POST':
        output = get_object_or_404(Output, pk=output_uuid)
        output.status = Output.OutputStatus.REJECTED
        output.save()
        messages.success(request, _('Rejected'))
        return render(
            request,
            'components/messages.html',
            {'from_htmx': True}
        )
    return HttpResponseBadRequest()
