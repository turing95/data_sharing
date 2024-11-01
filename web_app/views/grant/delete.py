from allauth.core.internal.http import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import DeleteView
from web_app.models import Grant
from django.contrib import messages
from django.utils.translation import gettext as _


class GrantDeleteView(LoginRequiredMixin, DeleteView):
    model = Grant
    pk_url_kwarg = "grant_uuid"

    def form_valid(self, form):
        self.object.delete()
        messages.success(self.request, _('Grant deleted successfully'))
        if self.request.GET.get('next'):
            return redirect(self.request.GET.get('next'))
        return redirect(reverse('grants', kwargs={'organization_uuid': self.object.organization.pk}))
