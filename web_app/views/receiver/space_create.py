from web_app.forms import SpaceForm,RequestFormSet
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from web_app.models import Sender


class SpaceFormView(FormView, LoginRequiredMixin):
    template_name = "receiver/space_create.html"
    form_class = SpaceForm
    success_url = reverse_lazy('spaces')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['requests'] = RequestFormSet(self.request.POST)
        else:
            data['requests'] = RequestFormSet()
        return data

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        context = self.get_context_data()
        requests = context['requests']

        space_instance = form.save(commit=False)
        space_instance.user = self.request.user
        space_instance.save()

        emails = form.cleaned_data['senders_emails']
        for email in emails:
            Sender.objects.create(email=email, space=space_instance)

        if requests.is_valid():
            requests.instance = space_instance
            requests.save()
        return super().form_valid(form)
