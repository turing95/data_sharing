from google.auth.transport.requests import Request
import arrow
from google.oauth2.credentials import Credentials
from django.conf import settings
from allauth.socialaccount.models import SocialToken
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from io import BytesIO


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
                    # should force user to reauthenticate
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

    def is_file_alive(self, file_id):
        try:
            file = self._service.files().get(supportsAllDrives=True, fileId=file_id,
                                             fields='id').execute()
            return (file.get('id', None) is not None) is True
        except Exception as e:
            return False

    def get_file_name(self, file_id):
        try:
            file = self._service.files().get(supportsAllDrives=True, fileId=file_id,
                                             fields='name').execute()
            return file.get('name', None)
        except Exception as e:
            return None

    def get_file_url(self, file_id):
        try:
            file = self._service.files().get(supportsAllDrives=True, fileId=file_id,
                                             fields='webViewLink').execute()
            return file.get('webViewLink', None)
        except Exception as e:
            return None

    def upload_file(self, file, file_name, folder_id):
        # Build the Drive service

        # File to be uploaded
        file_stream = BytesIO(file.read())
        file_stream.seek(0)

        # File to be uploaded
        file_metadata = {'name': file_name,
                         'parents': [folder_id]}
        media = MediaIoBaseUpload(file_stream,
                                  mimetype=file.content_type,
                                  resumable=True)

        # Upload the file
        file = self._service.files().create(supportsAllDrives=True, body=file_metadata,
                                            media_body=media,
                                            fields='id,webViewLink').execute()
        #return file.get('webViewLink', None)
        return file
