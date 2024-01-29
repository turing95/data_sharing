from django.contrib import messages
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView


class AccountDeleteView(LoginRequiredMixin, DeleteView):
    success_url = reverse_lazy('generic_home')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        user_pk = self.request.user.pk
        logout(self.request)
        User = get_user_model()
        User.objects.filter(pk=user_pk).delete()
        messages.success(self.request, 'Account successfully deleted')
        return super().form_valid(form)
