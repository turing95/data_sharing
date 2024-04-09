from django.views.generic import TemplateView

from web_app.mixins import CompanySideBarMixin, SubscriptionMixin, FieldTemplateMixin


class FieldTemplateDetailView(SubscriptionMixin, CompanySideBarMixin, FieldTemplateMixin, TemplateView):
    template_name = "private/company_templates/detail/base.html"
