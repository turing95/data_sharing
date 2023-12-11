from allauth.socialaccount.models import SocialAccount, SocialToken
from django.contrib.auth.models import User
from google.auth.transport.requests import Request

from google.oauth2.credentials import Credentials
import config


class CustomUser(User):
    class Meta:
        proxy = True

    def refresh_google_token(self):
        try:
            social_account = SocialAccount.objects.get(user=self, provider='google')
            token = SocialToken.objects.get(account=social_account)

            credentials = Credentials(
                token=token.token,
                refresh_token=token.token_secret,
                token_uri='https://accounts.google.com/o/oauth2/token',
                client_id=config.GOOGLE_CLIENT_ID,
                client_secret=config.GOOGLE_CLIENT_SECRET
            )

            if credentials.valid is False:
                credentials.refresh(Request())
                token.token = credentials.token
                token.token_secret = credentials.refresh_token
                token.expires_at = credentials.expiry
                token.save()  # Update the token in the database

            return token
        except (SocialAccount.DoesNotExist, SocialToken.DoesNotExist):
            # Handle the case where the user does not have a Google social account
            # or the token does not exist
            return None

    @property
    def google_token(self):
        return self.refresh_google_token()

    @property
    def google_credentials(self):
        token = self.refresh_google_token()
        if token:
            return Credentials(
                token=token.token,
                refresh_token=token.token_secret,
                token_uri='https://accounts.google.com/o/oauth2/token',
                client_id=config.GOOGLE_CLIENT_ID,
                client_secret=config.GOOGLE_CLIENT_SECRET
            )
        else:
            return None
