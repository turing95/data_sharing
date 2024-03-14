from django.views.generic import ListView

from web_app.mixins import CompanySideBarMixin, SubscriptionMixin, CompanyMixin, CompanyTabMixin


class CompanyContactsListView(SubscriptionMixin, CompanySideBarMixin, CompanyTabMixin, CompanyMixin, ListView):
    template_name = "private/company/detail/contacts_list.html"
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_tab']['contacts']['active'] = True
        return context

    def get_queryset(self):
        return self.get_company().spaces.order_by('created_at')
