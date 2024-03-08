from django.urls import reverse
from django.views.generic import FormView

from web_app.forms import CompanyForm
from web_app.mixins import CompanySideBarMixin, SubscriptionMixin, CompanyMixin, CompanyTabMixin


class CompanyDetailView(SubscriptionMixin, CompanySideBarMixin, CompanyTabMixin, CompanyMixin, FormView):
    template_name = "private/company/detail/base.html"
    form_class = CompanyForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_tab']['detail']['active'] = True
        return context

    def get_success_url(self):
        return reverse('companies', kwargs={'organization_uuid': self.get_company().organization.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_company()
        kwargs['organization'] = self.get_company().organization
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
