from allauth.socialaccount.models import SocialAccount, SocialToken
from django.contrib.auth.models import AbstractUser
from django.db import models
from google.auth.transport.requests import Request
import arrow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from msal import ConfidentialClientApplication
import requests
from django.conf import settings


class User(AbstractUser):
    '''
    Custom user model
    self.request.session['account_authentication_methods'] to access authentication methods( has social provider)
    '''
    organizations = models.ManyToManyField('Organization', through='UserOrganization')

    @property
    def full_name(self):
        return super().get_full_name()

    @property
    def google_account(self):
        try:
            return SocialAccount.objects.get(user=self, provider='custom_google')
        except SocialAccount.DoesNotExist:
            return None

    @property
    def microsoft_account(self):
        try:
            return SocialAccount.objects.get(user=self, provider='custom_microsoft')
        except SocialAccount.DoesNotExist:
            return None

    def get_folders(self, destination_type, folder_name=None):
        from web_app.models import OneDrive, GoogleDrive
        if destination_type == GoogleDrive.TAG:
            return GoogleService(self.google_account).get_folders(folder_name)
        elif destination_type == OneDrive.TAG:
            return MicrosoftService(self.microsoft_account).get_folders(folder_name)
        else:
            return None

    def refresh_google_token(self, token=None):
        return GoogleService(self.google_account).refresh_token(token)

    def refresh_microsoft_token(self, token=None):
        return MicrosoftService(self.microsoft_account).refresh_token(token)



class GoogleService:
    def __init__(self, social_account):
        self.social_account = social_account

    def refresh_token(self, token=None):
        try:
            if token is None:
                social_account = self.social_account
                if social_account is not None:
                    token = SocialToken.objects.get(account=social_account)
            if arrow.get(token.expires_at) < arrow.utcnow():
                credentials = Credentials(
                    token=token.token,
                    refresh_token=token.token_secret,
                    token_uri='https://accounts.google.com/o/oauth2/token',
                    client_id=settings.GOOGLE_CLIENT_ID,
                    client_secret=settings.GOOGLE_CLIENT_SECRET
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

    @property
    def _credentials(self):
        token = self.refresh_token()
        if token:
            return Credentials(
                token=token.token,
                refresh_token=token.token_secret,
                token_uri='https://accounts.google.com/o/oauth2/token',
                client_id=settings.GOOGLE_CLIENT_ID,
                client_secret=settings.GOOGLE_CLIENT_SECRET
            )
        else:
            return None

    @property
    def _service(self):
        return build('drive', 'v3', credentials=self._credentials)

    def get_folders(self, folder_name):
        credentials = self._credentials
        if not credentials:
            return None
        response = (
            self._service.files()
            .list(
                q="mimeType='application/vnd.google-apps.folder' and name contains '" + folder_name + "'",
                spaces="drive",
                fields="files(id, name)",
                supportsAllDrives=True
            )
            .execute()
        )
        return response.get('files', [])


class MicrosoftService:
    def __init__(self, social_account):
        self.social_account = social_account

    def refresh_token(self, token=None):
        if token is None:
            social_account = self.social_account
            if social_account is None:
                return None

            token = SocialToken.objects.get(account=social_account)
        if arrow.get(token.expires_at) < arrow.utcnow():
            # Create a Confidential Client Application
            app = ConfidentialClientApplication(
                settings.AZURE_CLIENT_ID,
                client_credential=settings.AZURE_CLIENT_SECRET
            )
            result = app.acquire_token_by_refresh_token(
                refresh_token=token.token_secret,
                scopes=[
                    "User.Read",  # access to user's account information
                    "Files.Read.All",
                    "Files.ReadWrite.All",  # access to user's files
                    "Sites.Read.All",  # access to user's sites
                    "Sites.ReadWrite.All",  # access to user's sites
                ],  # Specify the required scopes
            )
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

    def get_folders(self, folder_name=None):
        token = self.refresh_token()

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
        if response.status_code == 200:
            folders = [item for item in response.json().get('value', []) if 'folder' in item]
            return folders
        else:
            return None  # or handle the error as required


    def list_sites(self):
        token = self.refresh_token()
        url = "https://graph.microsoft.com/v1.0/sites/"
        headers = {
            'Authorization': f'Bearer {token.token}',
            'Content-Type': 'application/json'
        }
        response = requests.get(url, headers=headers)
        return response.json()