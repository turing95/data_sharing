from django.shortcuts import get_object_or_404, render

from web_app.forms import SpaceForm, RequestFormSet
from web_app.forms.space_create import DetailRequestFormSet
from web_app.models import Space, UploadRequest

from web_app.views import SpaceFormView


class SpaceDetailFormView(SpaceFormView):
    template_name = "private/space_detail.html"
    form_class = SpaceForm

    def get_context_data(self, **kwargs):
        data = super(SpaceFormView,self).get_context_data(**kwargs)
        if 'status' in self.request.GET:
            data['space_form'] = True
            data['file_name_tags'] = {'tags': [tag[1] for tag in UploadRequest.FileNameTag.choices]}
            data['requests'] = self.get_formset()
            data['status'] = self.request.GET.get('status')
        else:
            data['space'] = self.get_space()
        return data

    def get_success_url(self):
        return self.request.path

    def get_space(self):
        if not self._space:
            pk = self.kwargs.get('space_uuid')
            self._space = get_object_or_404(Space, pk=pk)
        return self._space

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_space()
        return kwargs

    def get_formset(self):
        queryset = self.get_space().requests.all()
        formset = DetailRequestFormSet(self.request.POST or None,
                                       queryset=queryset,
                                       instance=self.get_space(),
                                       initial=[{"title": req.title} for req in queryset])
        return formset
