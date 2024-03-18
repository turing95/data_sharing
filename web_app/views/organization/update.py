from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST

from web_app.models import Organization


@login_required
@require_POST
def organization_update(request,organization_uuid):
    organization = get_object_or_404(Organization, pk=organization_uuid)
    form = organization.form(request.POST)
    if form.is_valid():
        form.save()
    return redirect(reverse('organization_settings', kwargs={'organization_uuid': organization_uuid}))
