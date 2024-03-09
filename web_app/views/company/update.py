from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST

from web_app.models import Company


@login_required
@require_POST
def company_update(request, company_uuid):
    company = Company.objects.get(pk=company_uuid)
    if request.method == 'POST':
        form = company.form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse()
    return HttpResponseBadRequest()
