from django.views.generic import ListView

from web_app.mixins import CompanyMixin, CompanyTabMixin, CompanySideBarMixin, SubscriptionMixin
from web_app.models import File


class CompanyFilesListView(SubscriptionMixin, CompanySideBarMixin, CompanyTabMixin, CompanyMixin, ListView):
    template_name = "private/company/detail/files.html"
    model = File
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        return File.objects.filter(company=self.get_company())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_tab']['documents']['active'] = True
        return context
