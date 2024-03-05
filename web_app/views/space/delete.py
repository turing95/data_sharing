from allauth.core.internal.http import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import DeleteView


from web_app.models import Space


class DeleteSpaceView(LoginRequiredMixin, DeleteView):
    model = Space
    pk_url_kwarg = "space_uuid"


    def form_valid(self, form):
        self.object.is_deleted = True
        self.object.save()
        return redirect(reverse('spaces', kwargs={'organization_uuid': self.object.organization.pk}))
