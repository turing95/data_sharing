from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET

from web_app.models import TextField


@login_required
@require_GET
def text_field_detail(request, field_uuid):
    company_field = get_object_or_404(TextField, pk=field_uuid)
    return render(request,
                  'private/company/detail/field/fill_form.html',
                  {'field': company_field}
                  )