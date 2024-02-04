from allauth.socialaccount.providers.microsoft.provider import MicrosoftGraphProvider
from allauth.socialaccount import app_settings
from django.core.exceptions import ImproperlyConfigured


class CustomMicrosoftProvider(MicrosoftGraphProvider):
    id = 'custom_microsoft'
    name = 'Microsoft'

    def sociallogin_from_response(self, request, response):
        """
        Instantiates and populates a `SocialLogin` model based on the data
        retrieved in `response`. The method does NOT save the model to the
        DB.

        Data for `SocialLogin` will be extracted from `response` with the
        help of the `.extract_uid()`, `.extract_extra_data()`,
        `.extract_common_fields()`, and `.extract_email_addresses()`
        methods.

        :param request: a Django `HttpRequest` object.
        :param response: object retrieved via the callback response of the
            social auth provider.
        :return: A populated instance of the `SocialLogin` model (unsaved).
        """
        # NOTE: Avoid loading models at top due to registry boot...
        from allauth.socialaccount.adapter import get_adapter
        from allauth.socialaccount.models import SocialAccount, SocialLogin

        adapter = get_adapter()
        uid = self.extract_uid(response)
        if not isinstance(uid, str):
            raise ValueError(f"uid must be a string: {repr(uid)}")
        if len(uid) > app_settings.UID_MAX_LENGTH:
            raise ImproperlyConfigured(
                f"SOCIALACCOUNT_UID_MAX_LENGTH too small (<{len(uid)})"
            )

        extra_data = self.extract_extra_data(response)
        common_fields = self.extract_common_fields(response)
        socialaccount = SocialAccount(
            extra_data=extra_data,
            uid=uid,
            provider=(self.app.provider_id or self.app.provider)
            if self.app
            else self.id,
        )
        email_addresses = self.extract_email_addresses(response)
        self.cleanup_email_addresses(
            common_fields.get("email"),
            email_addresses,
            email_verified=common_fields.get("email_verified"),
        )
        sociallogin = SocialLogin(
            account=socialaccount, email_addresses=email_addresses
        )
        user = sociallogin.user = adapter.new_user(request, sociallogin)
        user.set_unusable_password()
        adapter.populate_user(request, sociallogin, common_fields)
        return sociallogin


provider_classes = [CustomMicrosoftProvider]
