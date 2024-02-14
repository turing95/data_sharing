
from allauth.socialaccount.providers.oauth2.views import OAuth2View, OAuth2LoginView

from allauth.socialaccount.providers.microsoft.views import MicrosoftGraphOAuth2Adapter
from .provider import CustomMicrosoftProvider
from custom_oauth_views import CustomOAuth2CallbackView

class CustomMicrosoftGraphOAuth2Adapter(MicrosoftGraphOAuth2Adapter):
    provider_id = CustomMicrosoftProvider.id


oauth2_login = OAuth2LoginView.adapter_view(CustomMicrosoftGraphOAuth2Adapter)
oauth2_callback = CustomOAuth2CallbackView.adapter_view(CustomMicrosoftGraphOAuth2Adapter)
