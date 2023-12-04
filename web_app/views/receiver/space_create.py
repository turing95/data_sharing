from web_app.forms import SpaceForm, RequestFormSet
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from web_app.models import Sender, GoogleDrive, UploadRequest
from allauth.socialaccount.models import SocialAccount, SocialToken


class SpaceFormView(LoginRequiredMixin, FormView):
    template_name = "private/space_create.html"
    form_class = SpaceForm
    success_url = reverse_lazy('spaces')
    _space = None  # Placeholder for the cached object

    def dispatch(self, request, *args, **kwargs):
        # Call the parent dispatch method
        response = super().dispatch(request, *args, **kwargs)
        response["Cross-Origin-Opener-Policy"] = "unsafe-none"
        return response

    def get_success_url(self):
        if self._space is not None:
            return reverse_lazy('receiver_space_detail', kwargs={'space_uuid': self._space.uuid})
        return super().get_success_url()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['space_form'] = True
        data['file_name_tags'] = {'tags':[tag[1] for tag in UploadRequest.FileNameTag.choices]}
        if self.request.POST:
            data['requests'] = RequestFormSet(self.request.POST)
        else:
            data['requests'] = RequestFormSet()
        return data

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        context = self.get_context_data()
        requests = context['requests']
        if requests.is_valid() is False:
            return super().form_invalid(form)

        space_instance = form.save(commit=False)
        space_instance.user = self.request.user
        space_instance.save()
        self._space = space_instance
        for email in form.cleaned_data.get('senders_emails', []):
            Sender.objects.create(email=email, space=space_instance)
        if requests.is_valid():
            requests.instance = space_instance
            requests.save()
            for req in requests:


                # TODO change when more than one possible type of dest
                GoogleDrive.create_from_folder_id(req.instance, req.cleaned_data.get('destination'),
                                                  req.cleaned_data.get('token'))
        else:
            print(requests.errors)
        return super().form_valid(form)
