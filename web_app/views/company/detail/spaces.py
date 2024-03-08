from django.views.generic import ListView
from web_app.mixins import CompanySideBarMixin, SubscriptionMixin, CompanyMixin, CompanyTabMixin



class CompanySpacesListView(SubscriptionMixin, CompanySideBarMixin, CompanyTabMixin, CompanyMixin, ListView):
    template_name = "private/company/detail/spaces_list.html"
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_tab']['spaces']['active'] = True
        return context

    def get_queryset(self):
        return self.get_company().spaces.filter(is_deleted=False).order_by('created_at')