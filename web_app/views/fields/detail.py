from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET

from web_app.models import TextField, FileField


@login_required
@require_GET
def text_field_detail(request, field_uuid):
    company_field = get_object_or_404(TextField, pk=field_uuid)
    return render(request,
                  'private/company/detail/field/text_fill_form.html',
                  {'field': company_field}
                  )


@login_required
@require_GET
def file_field_detail(request, field_uuid):
    company_field = get_object_or_404(FileField, pk=field_uuid)
    return render(request,
                  'private/company/detail/field/file_fill_form.html',
                  {'field': company_field}
                  )
