from web_app.forms import SpaceDetailForm
from django.views.generic.edit import FormView
from web_app.models import Space
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from django import forms


class SpaceDetailFormView(FormView,LoginRequiredMixin):
    template_name = "space_detail.html"
    form_class = SpaceDetailForm
    success_url = reverse_lazy('spaces')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        space = Space.objects.get(uuid=self.kwargs['space_uuid'])  # Retrieve the object from the database

        for index, space_req in enumerate(space.requests.all()):
            form.fields[f'file_{index}'] = forms.FileField()  # Dynamically adding file fields

        return form
