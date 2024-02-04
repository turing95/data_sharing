from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)

from .provider import CustomGoogleProvider


class CustomGoogleOAuth2Adapter(GoogleOAuth2Adapter):
    provider_id = CustomGoogleProvider.id


oauth2_login = OAuth2LoginView.adapter_view(CustomGoogleOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(CustomGoogleOAuth2Adapter)
