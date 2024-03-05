from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_GET
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, FormView

from web_app.forms import CompanyForm
from web_app.mixins import OrganizationMixin, SideBarMixin, SubscriptionMixin
from web_app.models import Company, Organization


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


# class CompanyCreateView(OrganizationMixin, CompanySideBarMixin, SubscriptionMixin, FormView):
#     template_name = "private/company/create.html"
#     form_class = CompanyForm

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


class CompanyTabMixin(SideBarMixin):
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['company_tab'] = {'spaces': False, 'detail': False}
        return data


class CompanyDetailView(SubscriptionMixin, CompanySideBarMixin, CompanyTabMixin, FormView):
    template_name = "private/company/detail.html"
    form_class = CompanyForm
    _company = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['organization'] = self.get_company().organization
        context['company'] = self.get_company()
        context['company_tab']['detail'] = True
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


class CompanySpacesListView(SubscriptionMixin, CompanySideBarMixin, CompanyTabMixin, ListView):
    template_name = "private/company/spaces_list.html"
    paginate_by = 12
    _company = None

    def get_company(self):
        if not self._company:
            self._company = Company.objects.get(pk=self.kwargs.get('company_uuid'))
        return self._company

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['organization'] = self.get_company().organization
        context['company'] = self.get_company()
        context['company_tab']['spaces'] = True
        return context

    def get_queryset(self):
        return self.get_company().spaces.filter(is_deleted=False).order_by('created_at')


@require_POST
@login_required
def search_companies(request, organization_uuid):
    companies = []
    if request.method == 'POST':
        organization = get_object_or_404(Organization, pk=organization_uuid)
        search_query = request.POST.get('search_company')
        if search_query:
            companies = organization.companies.filter(
                name__icontains=search_query
            )
        return render(request,
                      'private/space/create/components/company/results.html',
                      {'companies': companies})
    return HttpResponseBadRequest()



@login_required
@require_GET
def company_create(request, organization_uuid):
    company = Company.objects.create(name='New company',
                                 organization_id=organization_uuid)
    
    return redirect(reverse('company_detail', kwargs={'company_uuid': company.pk}))