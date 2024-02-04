from allauth.socialaccount.providers.oauth2.views import (
    OAuth2CallbackView,
    OAuth2LoginView,
)

from allauth.socialaccount.providers.microsoft.views import MicrosoftGraphOAuth2Adapter
from .provider import CustomMicrosoftProvider


class CustomMicrosoftGraphOAuth2Adapter(MicrosoftGraphOAuth2Adapter):
    provider_id = CustomMicrosoftProvider.id


oauth2_login = OAuth2LoginView.adapter_view(CustomMicrosoftGraphOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(CustomMicrosoftGraphOAuth2Adapter)