from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.http import require_POST

from web_app.models import Company


@login_required
@require_POST
def company_update_name(request, company_uuid):
    company = Company.objects.get(pk=company_uuid)
    if request.method == 'POST':
        form = company.name_form(request.POST)
        if form.is_valid():
            form.save()
        else:
            messages.error(request, form.errors['name'])
        return render(request, 'private/company/detail/company_name.html',
                      {'form': company.name_form(), 'from_htmx': True})
    return HttpResponseBadRequest()


@login_required
@require_POST
def company_update(request, company_uuid):
    company = Company.objects.get(pk=company_uuid)
    if request.method == 'POST':
        form = company.form(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'private/company/detail/company_form.html',
                          {'form': company.form()})
        return render(request, 'private/company/detail/company_form.html',
                      {'form': form})
    return HttpResponseBadRequest()
