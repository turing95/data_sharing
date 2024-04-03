from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET

from web_app.models import FieldGroup


@login_required
@require_GET
def group_elements(request, group_uuid):
    group = get_object_or_404(FieldGroup, pk=group_uuid)
    if request.GET.get('template'):
        return render(request,
                      'private/company_templates/detail/group/elements.html',
                      {'group': group}
                      )
    else:
        return render(request,
                      'private/company/detail/group/elements.html',
                      {'group': group}
                      )
