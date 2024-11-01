from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET

from web_app.models import Output


@login_required
@require_GET
def output_detail(request, output_uuid):
    return render(request, 'private/request/detail/output.html', {
        'output': get_object_or_404(Output, pk=output_uuid)
    })


@login_required
@require_GET
def output_reject_modal(request, output_uuid):
    return render(request, 'private/request/detail/output_reject_modal.html', {
        'output': get_object_or_404(Output, pk=output_uuid)
    })
