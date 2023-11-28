from web_app.forms import SpaceForm, RequestFormSet
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from web_app.models import Sender, Space
from allauth.socialaccount.models import SocialAccount, SocialToken


class SpaceFormView(LoginRequiredMixin, FormView):
    template_name = "receiver/private/space_create.html"
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
        data['google_access_token'] = self.get_google_access_token(self.request.user)
        data['picker_js'] = True
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
        self._space = space_instance

        if requests.is_valid():
            requests.instance = space_instance
            requests.save()
            for req in requests:
                for email in req.cleaned_data.get('senders_emails', []):
                    Sender.objects.create(email=email, request=req.instance)
        return super().form_valid(form)

    @staticmethod
    def get_google_access_token(user):
        '''try:
            # Assuming 'google' is the provider name you have used with allauth
            social_account = SocialAccount.objects.get(user=user, provider='google')
            token = SocialToken.objects.get(account=social_account)
            return token.token  # token.token is the access token
        except SocialAccount.DoesNotExist:
            # Handle the case where the user does not have a Google social account
            return None
        except SocialToken.DoesNotExist:
            # Handle the case where the token does not exist
            return None
        '''
        return None