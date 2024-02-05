from allauth.socialaccount.views import ConnectionsView as AllAuthConnectionsView
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from web_app.forms import UserForm


class ProfileView(FormView):
    success_url = reverse_lazy("account_settings")
    form_class = UserForm

    def get(self, request, *args, **kwargs):
        raise Http404()

    def post(self, request, *args, **kwargs):
        form = UserForm(self.request.POST or None, instance=self.request.user)
        if form.is_valid():
            form.save()
        return self.form_invalid(form)

    def form_invalid(self, form):
        return redirect(self.success_url)
