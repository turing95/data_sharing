from allauth.socialaccount.models import SocialAccount, SocialToken
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.functional import cached_property
from google.auth.transport.requests import Request
import arrow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from msal import ConfidentialClientApplication
import requests
from django.conf import settings
import jwt


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

    def get_folders(self, destination_type, folder_name=None, sharepoint_site=None):
        from web_app.models import OneDrive, GoogleDrive, SharePoint
        if destination_type == GoogleDrive.TAG:
            return GoogleService(self.google_account).get_folders(folder_name)
        elif destination_type == OneDrive.TAG or destination_type == SharePoint.TAG:
            return MicrosoftService(self.microsoft_account).get_folders(folder_name, sharepoint_site)
        else:
            return None

    def refresh_google_token(self,social_account=None, token=None):
        return GoogleService(social_account or self.google_account).refresh_token(token)

    def refresh_microsoft_token(self,social_account=None, token=None):
        return MicrosoftService(social_account or self.microsoft_account).refresh_token(token)

    @cached_property
    def sharepoint_sites(self):
        if self.microsoft_account is None or self.microsoft_account.socialtoken_set.count() == 0:
            return None
        return MicrosoftService(self.microsoft_account).get_sites()


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
                try:
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
                except Exception as e:
                    #should force user to reauthenticate
                    token.delete()
                    return None
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
        try:
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
                    token.delete()
                    return None
            return token
        except SocialToken.DoesNotExist:
            # Handle the case where the user does not have a Microsoft social account
            # or the token does not exist
            return None

    '''def _get_folders(self, folder_name=None,microsoft_site=None):
        THIS MIGHT BE USEFUL IN THE FUTURE, BUT ATM SEARCH FROM MSFT DOES NOT SEEM TO WORK THE WAY IT SHOULD
        token = self.refresh_token()

        headers = {
            'Authorization': f'Bearer {token.token}',
            'Content-Type': 'application/json'
        }
        # The URL for the Microsoft Graph API search endpoint
        url = 'https://graph.microsoft.com/beta/search/query'

        # The body of the request specifying the search query and entity types
        body = {
            "requests": [
                {
                    "entityTypes": ["driveItem"],
                    "query": {
                        "queryString": folder_name
                    },
                    "from": 0,
                    "size": 25
                }
            ]
        }

        # Send the POST request
        response = requests.post(url, headers=headers, json=body)
        if response.status_code == 200:
            results = response.json().get('value', [])
            folders = []
            for result in results:  # Loop through each result in the response
                # Each result may contain multiple hits, so we need to examine each one.
                for hit in result.get('hitsContainers', []):
                    # Each hit contains a resource which could be the item we are interested in.
                    for item in hit.get('hits', []):
                        # Now we examine the resource (item) to see if it is a folder.
                        # This assumes 'folder' information is part of the item's resourceData.
                        # Adjust the condition based on the actual structure of your items.
                        resource = item.get('resource', {})
                        folders.append(resource)
            return folders
        else:
            return self.search_personal_drive(folder_name)  # or handle the error as required'''

    def get_folders(self, folder_name=None, sharepoint_site=None):
        token = self.refresh_token()
        headers = {
            'Authorization': f'Bearer {token.token}',
            'Content-Type': 'application/json'
        }
        if sharepoint_site:
            url = f"https://graph.microsoft.com/v1.0/sites/{sharepoint_site}/drive/root/"
        else:
            url = "https://graph.microsoft.com/v1.0/me/drive/root/"
        if folder_name:
            url += f"search(q='{folder_name}')/"
        else:
            url += 'children'
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            folders = [item for item in response.json().get('value', []) if 'folder' in item]
            return folders
        else:
            return None  # or handle the error as required

    def get_sites(self):
        token = self.refresh_token()
        url = "https://graph.microsoft.com/v1.0/sites?search=*"
        headers = {
            'Authorization': f'Bearer {token.token}',
            'Content-Type': 'application/json'
        }
        response = requests.get(url, headers=headers)
        return response.json().get('value', [])

    @property
    def decoded_token(self):
        token = self.refresh_token()
        rs = jwt.decode(token.token, options={"verify_signature": False})
        return rs
