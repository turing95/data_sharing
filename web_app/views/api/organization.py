from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_POST

from web_app.forms import OrganizationForm

@require_GET
@login_required
def create_organization_modal(request):
    if request.method == 'GET':
        form = OrganizationForm()
        return render(request,
                      'private/organization/create_modal.html', {'form': form})

    return HttpResponseBadRequest()


@require_POST
@login_required
def create_organization(request):
    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            organization = form.save(commit=False)
            organization.created_by = request.user
            organization.save()
            request.user.organizations.add(organization)
            messages.success(request, 'Organization created successfully')
            return render(request,
                          'private/organization/create_form.html',
                          {'form': OrganizationForm(), 'show_msg': True, 'from_htmx': True})
        messages.error(request, 'Error creating contact. Please try again.')
        return render(request,
                      'private/organization/create_form.html',
                      {'form': form, 'show_msg': True, 'from_htmx': True},
                      status=400
                      )
    return HttpResponseBadRequest()



