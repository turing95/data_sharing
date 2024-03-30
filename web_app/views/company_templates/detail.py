from django.views.generic import TemplateView

from web_app.mixins import CompanySideBarMixin, SubscriptionMixin, CompanyTemplateMixin


class CompanyTemplateDetailView(SubscriptionMixin, CompanySideBarMixin, CompanyTemplateMixin, TemplateView):
    template_name = "private/company_templates/detail/base.html"
