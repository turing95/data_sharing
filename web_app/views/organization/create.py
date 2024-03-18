from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST
from django.utils.translation import gettext_lazy as _
from web_app.forms import OrganizationCreateForm


@require_GET
@login_required
def create_organization_modal(request):
    if request.method == 'GET':
        form = OrganizationCreateForm()
        return render(request,
                      'private/organization/create_modal.html', {'form': form})

    return HttpResponseBadRequest()


@require_POST
@login_required
def create_organization(request):
    if request.method == 'POST':
        form = OrganizationCreateForm(request.POST)
        if form.is_valid():
            organization = form.save(commit=False)
            organization.created_by = request.user
            organization.save()
            request.user.organizations.add(organization)
            messages.success(request, _('Organization created successfully'))
            return redirect(reverse('spaces', kwargs={'organization_uuid': organization.pk}))
        messages.error(request, _('Error creating organization. Please try again.'))
        return redirect(reverse('spaces'))
    return HttpResponseBadRequest()
