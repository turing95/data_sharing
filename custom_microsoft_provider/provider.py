from allauth.socialaccount.providers.microsoft.provider import MicrosoftGraphProvider
from allauth.socialaccount import app_settings
from django.core.exceptions import ImproperlyConfigured


class CustomMicrosoftProvider(MicrosoftGraphProvider):
    id = 'custom_microsoft'
    name = 'Microsoft'

provider_classes = [CustomMicrosoftProvider]
