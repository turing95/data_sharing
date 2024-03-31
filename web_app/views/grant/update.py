from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.http import require_POST

from web_app.models import Grant

@login_required
@require_POST
def grant_update_name(request, grant_uuid):
    grant = Grant.objects.get(pk=grant_uuid)
    if request.method == 'POST':
        form = grant.name_form(request.POST)
        if form.is_valid():
            form.save()
        else:
            messages.error(request, form.errors['name'])
        return render(request, 'private/grant/grant_name.html',
                      {'form': grant.name_form(), 'from_htmx': True})
    return HttpResponseBadRequest()


@login_required
@require_POST
def grant_update(request, grant_uuid):
    grant = Grant.objects.get(pk=grant_uuid)
    if request.method == 'POST':
        form = grant.form(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'private/grant/grant_form.html',
                          {'form': grant.form()})
        return render(request, 'private/grant/grant_form.html',
                      {'form': form})
    return HttpResponseBadRequest()
