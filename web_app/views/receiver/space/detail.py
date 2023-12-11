from django.shortcuts import get_object_or_404, render
from web_app.forms import SpaceForm, DetailRequestFormSet
from web_app.models import Space, UploadRequest, Sender

from web_app.views import SpaceFormView


class SpaceDetailFormView(SpaceFormView):
    template_name = "private/space_detail.html"
    form_class = SpaceForm

    def get_context_data(self, **kwargs):
        data = super(SpaceFormView, self).get_context_data(**kwargs)
        if 'status' in self.request.GET:
            data = self.get_context_for_form(data, button_text='Update space', status=self.request.GET.get('status'))
        else:
            data['space'] = self.get_space()
        return data

    def handle_senders(self, senders_emails, space_instance):

        existing_senders = {sender.email: sender for sender in space_instance.senders.all()}

        # Add or update senders
        for email in senders_emails:
            email = email.strip()
            if email in existing_senders:
                del existing_senders[email]
            else:
                Sender.objects.create(email=email, space=space_instance)
        # Delete removed emails
        for email, sender in existing_senders.items():
            print('deleting', email, sender)
            sender.delete()

    def get_success_url(self):
        return self.request.get_full_path()

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
        formset = DetailRequestFormSet(self.request.POST or None,
                                       instance=self.get_space(),form_kwargs={'access_token': self.request.custom_user.google_token.token})
        return formset
