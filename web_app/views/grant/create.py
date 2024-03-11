from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.shortcuts import redirect
from django.views.decorators.http import require_GET
from web_app.models import Organization, Grant


@login_required
@require_GET
def grant_create(request, organization_uuid):
    organization = get_object_or_404(Organization, pk=organization_uuid)
    grant = Grant.objects.create(organization=organization)
    return redirect(reverse('grant_detail', kwargs={'grant_uuid': grant.pk}))