from allauth.core.internal.http import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DeleteView
from web_app.models import CompanyTemplate
from django.contrib import messages
from django.utils.translation import gettext as _


class CompanyTemplateDeleteView(LoginRequiredMixin, DeleteView):
    model = CompanyTemplate
    pk_url_kwarg = "company_template_uuid"


    def form_valid(self, form):
        self.object.delete()
        messages.success(self.request, _('Company template deleted successfully'))
        if self.request.GET.get('next'):
            return redirect(self.request.GET.get('next'))
        return redirect(reverse('company_templates', kwargs={'organization_uuid': self.object.organization.pk}))