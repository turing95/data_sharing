from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns

from .provider import CustomMicrosoftProvider


urlpatterns = default_urlpatterns(CustomMicrosoftProvider)
