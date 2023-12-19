from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from web_app.models import Space


class DeleteSpaceView(LoginRequiredMixin, DeleteView):
    model = Space
    success_url = reverse_lazy('spaces')
    pk_url_kwarg = "space_uuid"

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.is_deleted = True
        self.object.save()
        return HttpResponseRedirect(success_url)
