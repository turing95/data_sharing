from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from django.views.generic import FormView

from web_app.forms import CompanyCreateForm
from web_app.mixins import OrganizationMixin, CompanySideBarMixin, SubscriptionMixin
from web_app.models import Company


class CompanyCreateView(OrganizationMixin, CompanySideBarMixin, SubscriptionMixin, FormView):
    template_name = "private/company/create.html"
    form_class = CompanyCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('companies', kwargs={'organization_uuid': self.get_organization().pk})

    def get(self, request, *args, **kwargs):
        company = Company.objects.create(name='New company',
                                         organization=self.get_organization())

        return redirect(reverse('company_detail', kwargs={'company_uuid': company.pk}))
    def form_valid(self, form):
        company = form.save(commit=False)
        company.organization = self.get_organization()
        company.save()
        if self.request.headers.get('HX-Request'):
            messages.success(self.request, _('Company created'))
            return render(self.request, 'components/messages.html', {'from_htmx': True})
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('HX-Request'):
            messages.error(self.request, _('Company not created'))
            return render(self.request, 'components/messages.html', {'from_htmx': True})
        return super().form_invalid(form)
