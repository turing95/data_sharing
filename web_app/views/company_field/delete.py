from django.shortcuts import render
from django.views.decorators.http import require_POST, require_GET
from web_app.models import CompanyField, Company
from django.http import HttpResponseBadRequest
from web_app.forms import CompanyFieldSetForm, CompanyFieldFillForm
from web_app.mixins import SideBarMixin, SubscriptionMixin, CompanyMixin
from django.views.generic import FormView

from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseBadRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect
# import soemthing to render html in a string
from django.template.loader import render_to_string

@require_POST
@login_required
def company_field_delete(request, company_field_uuid):
    field = CompanyField.objects.get(pk=company_field_uuid)
    company= field.company
    field.delete()
    messages.success(request, _('Field removed successfully'))
    return HttpResponse('')
