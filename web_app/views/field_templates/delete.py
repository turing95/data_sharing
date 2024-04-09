from allauth.core.internal.http import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DeleteView
from web_app.models import FieldTemplate
from django.contrib import messages
from django.utils.translation import gettext as _


class FieldTemplateDeleteView(LoginRequiredMixin, DeleteView):
    model = FieldTemplate
    pk_url_kwarg = "template_uuid"

    def form_valid(self, form):
        self.object.delete()
        messages.success(self.request, _('Template deleted successfully'))
        if self.request.GET.get('next'):
            return redirect(self.request.GET.get('next'))
        return redirect(reverse('field_group_templates', kwargs={'organization_uuid': self.object.organization.pk}))
