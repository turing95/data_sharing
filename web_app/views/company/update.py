from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST

from web_app.models import Company
from web_app.forms import CompanyUpdateForm


@login_required
@require_POST
def company_update(request, company_uuid):
    company = Company.objects.get(pk=company_uuid)
    if request.method == 'POST':
        form = CompanyUpdateForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            return HttpResponse()
    return HttpResponseBadRequest()
