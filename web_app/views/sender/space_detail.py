from web_app.forms import SpaceDetailForm
from django.views.generic.edit import FormView
from web_app.models import Sender
from django.urls import reverse_lazy

from django import forms


class SpaceDetailFormView(FormView):
    template_name = "sender/space_detail.html"
    form_class = SpaceDetailForm
    success_url = reverse_lazy('spaces')

    def form_valid(self, form):
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        space = Sender.objects.get(uuid=self.kwargs['sender_uuid']).space

        for index, space_req in enumerate(space.requests.all()):
            form.fields[f'file_{index}'] = forms.FileField()

        return form