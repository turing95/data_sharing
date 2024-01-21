from allauth.socialaccount.models import SocialAccount, SocialToken
from django.contrib.auth.models import User
from google.auth.transport.requests import Request
import arrow
from google.oauth2.credentials import Credentials
from msal import ConfidentialClientApplication
import requests
import config


class CustomUser(User):
    class Meta:
        proxy = True

    def google_account(self):
        try:
            return SocialAccount.objects.get(user=self, provider='google')
        except SocialAccount.DoesNotExist:
            return None

    def microsoft_account(self):
        try:
            return SocialAccount.objects.get(user=self, provider='microsoft')
        except SocialAccount.DoesNotExist:
            return None

    def get_one_drive_folders(self,folder_name=None):
        token = self.microsoft_token
        print(token)
        if not token:
            return None  # or handle the error as required

        headers = {
            'Authorization': f'Bearer {token.token}',
            'Content-Type': 'application/json'
        }
        url = "https://graph.microsoft.com/v1.0/me/drive/root/"
        if folder_name:
            url += f"search(q='{folder_name}')"
        else:
            url += 'children'

        response = requests.get(url, headers=headers)
        print(response.json())
        if response.status_code == 200:
            folders = [item for item in response.json().get('value', []) if 'folder' in item]
            return folders
        else:
            return None  # or handle the error as required

    def refresh_google_token(self):
        try:
            social_account = self.google_account()
            if social_account is not None:
                token = SocialToken.objects.get(account=social_account)
                if arrow.get(token.expires_at) < arrow.utcnow():
                    credentials = Credentials(
                        token=token.token,
                        refresh_token=token.token_secret,
                        token_uri='https://accounts.google.com/o/oauth2/token',
                        client_id=config.GOOGLE_CLIENT_ID,
                        client_secret=config.GOOGLE_CLIENT_SECRET
                    )
                    credentials.refresh(Request())
                    token.token = credentials.token
                    token.expires_at = credentials.expiry
                    token.save()  # Update the token in the database

                return token
        except SocialToken.DoesNotExist:
            # Handle the case where the user does not have a Google social account
            # or the token does not exist
            return None

    def refresh_microsoft_token(self):
        social_account = self.microsoft_account()
        if social_account is None:
            return None

        token = SocialToken.objects.get(account=social_account)
        if arrow.get(token.expires_at) < arrow.utcnow():
            # Create a Confidential Client Application
            app = ConfidentialClientApplication(
                config.AZURE_CLIENT_ID,
                client_credential=config.AZURE_CLIENT_SECRET,
                authority=f'https://login.microsoftonline.com/{config.AZURE_TENANT_ID}',
                validate_authority=True
            )
            result = app.acquire_token_by_refresh_token(
                refresh_token=token.token_secret,
                scopes=[
                    "User.Read",  # access to user's account information
                    "Files.ReadWrite.All",  # access to user's files
                ],  # Specify the required scopes
            )
            print(result)
            if 'access_token' in result:
                # Update token details from result
                token.token = result['access_token']
                token.expires_at = arrow.utcnow().shift(seconds=result['expires_in']).datetime
                token.save()  # Update the token in the database

                return token
            else:
                # Handle error or no new token returned
                return None
        return token

    @property
    def google_token(self):
        return self.refresh_google_token()

    @property
    def microsoft_token(self):
        return self.refresh_microsoft_token()

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
