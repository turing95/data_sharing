from django.shortcuts import get_object_or_404

from web_app.forms.receiver_space_detail import SpaceDetailForm
from django.views.generic.edit import FormView
from web_app.models import Space

from django import forms


class SpaceDetailFormView(FormView):
    template_name = "receiver/space_detail.html"
    form_class = SpaceDetailForm
    _object = None  # Placeholder for the cached object

    def get_success_url(self):
        return self.request.path

    def form_valid(self, form):
        # Update the object with the form data
        space = self.get_object()
        space.name = form.cleaned_data['name']
        space.save()
        return super().form_valid(form)

    def get_object(self):
        if not self._object:
            pk = self.kwargs.get('space_uuid')
            self._object = get_object_or_404(Space, pk=pk)
        return self._object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['space'] = self.get_object()
        return context

    def get_initial(self):
        # Initialize the form with the current state of the object
        return {
            'name': self.get_object().name,
        }
