from allauth.core.internal.http import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import DeleteView
from web_app.models import Company
from django.contrib import messages
from django.utils.translation import gettext as _


class CompanyDeleteView(LoginRequiredMixin, DeleteView):
    model = Company
    pk_url_kwarg = "company_uuid"


    def form_valid(self, form):
        self.object.delete()
        messages.success(self.request, _('Company deleted successfully'))
        return redirect(reverse('companies', kwargs={'organization_uuid': self.object.organization.pk}))