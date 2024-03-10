from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.http import require_POST
from web_app.models import CompanyField


@login_required
@require_POST
def company_field_update(request, company_field_uuid):
    if request.method == 'POST':
        company_field = CompanyField.objects.get(pk=company_field_uuid)
        form = company_field.form(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'private/company/detail/company_field.html',
                          {'form': company_field.form()})
        return render(request, 'private/company/detail/company_field.html',
                      {'form': form})
    return HttpResponseBadRequest()

