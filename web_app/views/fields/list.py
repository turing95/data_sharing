from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET, require_POST

from web_app.models import FieldGroup, GroupElement


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

@login_required
@require_POST
def group_elements_update_order(request, group_uuid):
    group = get_object_or_404(FieldGroup, pk=group_uuid)
    for i, uuid in enumerate(request.POST.getlist('group_element_order[]')):
        group_element = GroupElement.objects.get(pk=uuid)
        group_element.position = i + 1
        group_element.save()

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

