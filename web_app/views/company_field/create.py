from django.contrib.auth.decorators import login_required
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
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string


class CompanyFieldCreateView(CompanyMixin, SideBarMixin,  SubscriptionMixin, FormView):
    template_name = "private/company/detail/field/create_update_modal.html"
    form_class = CompanyFieldSetForm

    def form_valid(self, form):
        field = form.save(commit=False)
        field.company = self.get_company()
        field.save()
        messages.success(self.request, _('New field created successfully'))
        response = render(self.request, 'private/company/detail/field/fill_form.html',  {'field': field})
        response['HX-Trigger'] = 'closeModal'
        return response

    def form_invalid(self, form): 
        if self.request.headers.get('HX-Request'):
            return render(self.request,
                          'private/company/detail/field/set_form.html',
                          {'form': form, 'show_msg': True, 'from_htmx': True, 'company_uuid': self.get_company().pk, 'confirm_button_text': _('Create field')}
                          )
    
        return super().form_invalid(form)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['company'] = self.get_company()
        return kwargs

@require_GET
@login_required
def company_field_create_modal(request, company_uuid):
    if request.method == 'GET':
        company = get_object_or_404(Company, pk=company_uuid)            
        form = CompanyFieldSetForm(company=company)
        
        return render(request,
                      'private/company/detail/field/create_update_modal.html',
                      {'form': form,
                      'company_uuid': company_uuid,
                      'confirm_button_text': _('Create field'),
                        })

    return HttpResponseBadRequest()