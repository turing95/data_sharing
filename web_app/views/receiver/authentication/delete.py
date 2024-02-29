from django.contrib import messages
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from web_app.models import Space, UploadRequest, GenericDestination


class AccountDeleteView(LoginRequiredMixin, DeleteView):
    success_url = reverse_lazy('generic_home')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        user_pk = self.request.user.pk
        logout(self.request)
        User = get_user_model()
        user = User.objects.get(pk=user_pk)
        spaces_to_delete = Space.objects.filter(user_id=user_pk,organization__in=user.created_organizations.all())
        UploadRequest.objects.filter(space__in=spaces_to_delete).update(is_active=False)
        dests = GenericDestination.objects.filter(user=user)
        UploadRequest.objects.filter(destinations__in=dests).update(is_active=False)
        dests.update(is_active=False)
        spaces_to_delete.update(is_deleted=True)
        user.delete()
        messages.success(self.request, 'Account successfully deleted')
        return super().form_valid(form)
