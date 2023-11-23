from web_app.forms import SpaceForm
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class SpaceFormView(FormView, LoginRequiredMixin):
    template_name = "space_create.html"
    form_class = SpaceForm
    success_url = reverse_lazy('spaces')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        form.save()
        return super().form_valid(form)
