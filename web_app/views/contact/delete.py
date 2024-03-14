from allauth.core.internal.http import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import DeleteView
from web_app.models import Contact
from django.contrib import messages
from django.utils.translation import gettext as _


class DeleteContactView(LoginRequiredMixin, DeleteView):
    model = Contact
    pk_url_kwarg = "contact_uuid"


    def form_valid(self, form):
        self.object.delete()
        messages.success(self.request, _('Contact deleted successfully'))
        return redirect(reverse('contacts', kwargs={'organization_uuid': self.object.organization.pk}))