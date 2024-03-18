from allauth.core.internal.http import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DeleteView

from web_app.models import Organization


class OrganizationDeleteView(LoginRequiredMixin, DeleteView):
    model = Organization
    pk_url_kwarg = "organization_uuid"

    def form_valid(self, form):
        self.object.delete()
        return redirect(reverse('organizations', kwargs={'organization_uuid': self.object.organization.pk}))
