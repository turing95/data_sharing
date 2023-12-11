from allauth.socialaccount.models import SocialAccount, SocialToken

from web_app.forms import SpaceForm, RequestFormSet
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from web_app.models import Sender, GoogleDrive, UploadRequest, UploadRequestFileType
from django.db import transaction
from web_app.tasks.notifications import sender_invite


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

    def get_context_for_form(self, data, button_text='Create space', **kwargs):
        data['space_form'] = True
        data['file_name_tags'] = {'tags': [tag[1] for tag in UploadRequest.FileNameTag.choices]}
        data['requests'] = self.get_formset()
        data['submit_text'] = button_text
        data['google_user_data'] = {'accessToken': self.get_google_access_token()}
        data.update(kwargs)
        return data

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        return self.get_context_for_form(data)

    def get_formset(self):
        return RequestFormSet(self.request.POST or None)

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        formset = self.get_formset()

        if form.is_valid():
            print('form valid')
            space_instance = form.save(commit=False)
            space_instance.user = request.user
            formset.instance = space_instance

            if formset.is_valid():
                print('formset valid')

                with transaction.atomic():
                    space_instance.save()
                    self._space = space_instance
                    self.handle_senders(form.cleaned_data.get('senders_emails', []), space_instance)
                    self.handle_formset(formset)
                return self.form_valid(form)
        else:
            print('form invalid')
            print(form.errors)
            print(formset.errors)
        return self.form_invalid(form)

    @staticmethod
    def handle_senders(emails, space_instance):
        for email in emails:
            sender = Sender.objects.create(email=email, space=space_instance)
            sender_invite.delay(sender.pk)

    @staticmethod
    def handle_formset(formset):
        formset.save()
        for req in formset:
            GoogleDrive.create_from_folder_id(req.instance, req.cleaned_data.get('destination'),
                                              req.cleaned_data.get('token'))

    def get_google_access_token(self):
        try:
            # Assuming 'google' is the provider name you have used with allauth
            social_account = SocialAccount.objects.get(user=self.request.user, provider='google')
            token = SocialToken.objects.get(account=social_account)
            return token.token  # token.token is the access token
        except SocialAccount.DoesNotExist:
            # Handle the case where the user does not have a Google social account
            return None
        except SocialToken.DoesNotExist:
            # Handle the case where the token does not exist
            return None
