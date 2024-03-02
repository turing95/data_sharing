from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, FormView

from web_app.forms import CompanyForm
from web_app.mixins import OrganizationMixin, SideBarMixin, SubscriptionMixin
from web_app.models import Company


class CompanySideBarMixin(SideBarMixin):
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['sidebar']['company'] = True
        return data


class CompanyListView(OrganizationMixin, CompanySideBarMixin, SubscriptionMixin, ListView):
    template_name = "private/company/list.html"
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return self.get_organization().companies.all().order_by('created_at')


class CompanyCreateView(OrganizationMixin, CompanySideBarMixin, SubscriptionMixin, CreateView):
    template_name = "private/company/create.html"
    model = Company
    fields = ['name']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('companies', kwargs={'organization_uuid': self.get_organization().pk})

    def form_valid(self, form):
        company = form.save(commit=False)
        company.organization = self.get_organization()
        company.save()
        return super().form_valid(form)


class CompanyDetailView(SubscriptionMixin, CompanySideBarMixin, FormView):
    template_name = "private/company/detail.html"
    form_class = CompanyForm
    _company = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['organization'] = self.get_company().organization
        context['company'] = self.get_company()
        '''context['back'] = {'url': reverse_lazy('companies', kwargs={'organization_uuid': self.get_company().organization.pk}),
                        'text': 'Back to Companies'}'''
        return context

    def get_company(self):
        if not self._company:
            self._company = Company.objects.get(pk=self.kwargs.get('company_uuid'))
        return self._company

    def get_success_url(self):
        return reverse('companies', kwargs={'organization_uuid': self.get_company().organization.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_company()
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
