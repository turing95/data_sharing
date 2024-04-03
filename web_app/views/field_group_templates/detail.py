from django.views.generic import TemplateView

from web_app.mixins import CompanySideBarMixin, SubscriptionMixin, FieldGroupTemplateMixin


class FieldGroupTemplateDetailView(SubscriptionMixin, CompanySideBarMixin, FieldGroupTemplateMixin, TemplateView):
    template_name = "private/company_templates/detail/base.html"
