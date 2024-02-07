from allauth.socialaccount.providers.google.provider import GoogleProvider
from allauth.socialaccount import app_settings
from django.core.exceptions import ImproperlyConfigured


class CustomGoogleProvider(GoogleProvider):
    id = 'custom_google'
    name = 'Google'


provider_classes = [CustomGoogleProvider]
