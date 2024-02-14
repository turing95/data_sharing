from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.views import OAuth2View, OAuth2LoginView

from custom_oauth_views import CustomOAuth2CallbackView
from .provider import CustomGoogleProvider


class CustomGoogleOAuth2Adapter(GoogleOAuth2Adapter):
    provider_id = CustomGoogleProvider.id


oauth2_login = OAuth2LoginView.adapter_view(CustomGoogleOAuth2Adapter)
oauth2_callback = CustomOAuth2CallbackView.adapter_view(CustomGoogleOAuth2Adapter)
