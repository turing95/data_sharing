from allauth.socialaccount.adapter import get_adapter
from allauth.socialaccount.providers.oauth2.views import OAuth2View
from django.contrib import messages
from django.shortcuts import redirect
from requests import RequestException
from django.utils.translation import gettext_lazy as _

from django.core.exceptions import PermissionDenied
from allauth.socialaccount.helpers import (
    complete_social_login,
    render_authentication_error,
)
from allauth.socialaccount.models import SocialLogin, SocialAccount
from allauth.socialaccount.providers.base import ProviderException
from allauth.socialaccount.providers.base.constants import (
    AuthError,
)
from allauth.socialaccount.providers.oauth2.client import (
    OAuth2Error,
)
from allauth.utils import get_request_param


class CustomOAuth2CallbackView(OAuth2View):
    def dispatch(self, request, *args, **kwargs):
        if "error" in request.GET or "code" not in request.GET:
            # Distinguish cancel from error
            auth_error = request.GET.get("error", None)
            if auth_error == self.adapter.login_cancelled_error:
                error = AuthError.CANCELLED
            else:
                error = AuthError.UNKNOWN
            return render_authentication_error(
                request, self.adapter.provider_id, error=error
            )
        app = self.adapter.get_provider().app
        client = self.get_client(self.request, app)

        try:
            access_token = self.adapter.get_access_token_data(request, app, client)
            token = self.adapter.parse_token(access_token)
            if app.pk:
                token.app = app
            login = self.adapter.complete_login(
                request, app, token, response=access_token
            )
            login.token = token
            if self.adapter.supports_state:
                login.state = SocialLogin.verify_and_unstash_state(
                    request, get_request_param(request, "state")
                )
            else:
                login.state = SocialLogin.unstash_state(request)
            if request.user.is_authenticated:
                existing_social_accounts = SocialAccount.objects.filter(provider=login.account.provider,
                                                                        user=request.user)
                if (existing_social_accounts.exists() and
                        not existing_social_accounts.filter(uid=login.account.uid).exists()):
                    provider = self.adapter.get_provider()
                    messages.error(request,
                                   _(f"You already have an account with {provider.name}, reconnect or disconnect the existing one."))
                    default_next = get_adapter().get_connect_redirect_url(request, login.account)
                    next_url = login.get_redirect_url(request) or default_next
                    return redirect(next_url)

            return complete_social_login(request, login)
        except (
                PermissionDenied,
                OAuth2Error,
                RequestException,
                ProviderException,
        ) as e:
            return render_authentication_error(
                request, self.adapter.provider_id, exception=e
            )
