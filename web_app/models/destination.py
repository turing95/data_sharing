import requests
from django.contrib.contenttypes.models import ContentType

from web_app.models import PolymorphicRelationModel, BaseModel, ActiveModel
from django.db import models
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from io import BytesIO


class GenericDestination(PolymorphicRelationModel, ActiveModel):
    tag = models.CharField(max_length=50)
    request = models.ForeignKey('UploadRequest', on_delete=models.CASCADE, related_name='destinations')

    def __str__(self):
        return self.tag

    @property
    def folder_id(self):
        return self.related_object.folder_id

    @property
    def name(self):
        return self.related_object.name

    @property
    def url(self):
        return self.related_object.url

    def upload_file(self, file, file_name):
        return self.related_object.upload_file(file, file_name)

    @classmethod
    def create_from_folder_id(cls, request_instance, destination_type, folder_id):
        if destination_type == GoogleDrive.TAG:
            return GoogleDrive.create_from_folder_id(request_instance, folder_id)
        elif destination_type == OneDrive.TAG:
            return OneDrive.create_from_folder_id(request_instance, folder_id)
        else:
            raise NotImplementedError


class GoogleDrive(BaseModel):
    TAG = 'google_drive'
    folder_id = models.CharField(max_length=255)
    PROVIDER_ID = 'google'

    @classmethod
    def create_from_folder_id(cls, upload_request, folder_id):
        google_drive_destination = cls(folder_id=folder_id)

        generic_destination = GenericDestination(
            request=upload_request,
            content_type=ContentType.objects.get_for_model(cls),
            object_id=google_drive_destination.pk,
            tag=cls.TAG,
        )

        generic_destination.save()
        google_drive_destination.save()

        return generic_destination

    @property
    def service(self):
        return build('drive', 'v3', credentials=self.custom_user.google_credentials)

    @property
    def name(self):
        file = self.service.files().get(supportsAllDrives=True, fileId=self.folder_id,
                                        fields='name').execute()
        return file.get('name')

    @property
    def url(self):
        return f'https://drive.google.com/drive/folders/{self.folder_id}'

    def upload_file(self, file, file_name):
        # Build the Drive service

        # File to be uploaded
        file_stream = BytesIO(file.read())
        file_stream.seek(0)

        # File to be uploaded
        file_metadata = {'name': file_name,
                         'parents': [self.folder_id]}
        media = MediaIoBaseUpload(file_stream,
                                  mimetype=file.content_type,
                                  resumable=True)

        # Upload the file
        file = self.service.files().create(supportsAllDrives=True, body=file_metadata,
                                           media_body=media,
                                           fields='id,webViewLink').execute()
        return file.get('webViewLink')

    @property
    def generic_destination(self):
        return GenericDestination.objects.get(
            content_type=ContentType.objects.get_for_model(self.__class__),
            object_id=self.pk,
        )

    @property
    def user(self):
        return self.generic_destination.request.space.user

    @property
    def custom_user(self):
        from web_app.models import CustomUser
        return CustomUser.objects.get(pk=self.user.pk)


class OneDrive(BaseModel):
    TAG = 'one_drive'
    folder_id = models.CharField(max_length=255)
    PROVIDER_ID = 'microsoft'

    @classmethod
    def create_from_folder_id(cls, upload_request, folder_id):
        one_drive_destination = cls(folder_id=folder_id)

        generic_destination = GenericDestination(
            request=upload_request,
            content_type=ContentType.objects.get_for_model(cls),
            object_id=one_drive_destination.pk,
            tag=cls.TAG,
        )

        generic_destination.save()
        one_drive_destination.save()

        return generic_destination

    @property
    def generic_destination(self):
        return GenericDestination.objects.get(
            content_type=ContentType.objects.get_for_model(self.__class__),
            object_id=self.pk,
        )

    def upload_file(self, file, file_name):
        # Ensure you have a valid access token
        token = self.custom_user.microsoft_token
        if not token:
            raise Exception("No valid Microsoft token available.")

        # Set up headers for the request
        headers = {
            'Authorization': f'Bearer {token.token}',
            'Content-Type': file.content_type,  # Assuming 'file' is a Django UploadedFile object
        }

        # Prepare the file stream
        file_stream = BytesIO(file.read())
        file_stream.seek(0)

        # Construct the URL for the file upload
        url = f"https://graph.microsoft.com/v1.0/me/drive/items/{self.folder_id}:/{file_name}:/content"

        # Send the request to upload the file
        response = requests.put(url, headers=headers, data=file_stream)

        # Check if the upload was successful
        if response.status_code in [200, 201]:
            return response.json().get('webUrl')  # Returns the URL of the uploaded file
        else:
            # Handle any errors that occur during the upload
            raise Exception(f"Failed to upload file: {response.json()}")

    @property
    def user(self):
        return self.generic_destination.request.space.user

    @property
    def custom_user(self):
        from web_app.models import CustomUser
        return CustomUser.objects.get(pk=self.user.pk)

    @property
    def url(self):
        print('getting url')
        token = self.custom_user.microsoft_token
        if not token:
            return None

        headers = {
            'Authorization': f'Bearer {token.token}'
        }
        url = f"https://graph.microsoft.com/v1.0/me/drive/items/{self.folder_id}"

        response = requests.get(url, headers=headers)
        print(response.json())
        if response.status_code == 200:
            data = response.json()
            return data.get('webUrl')  # The URL of the folder
        else:
            return None

    @property
    def name(self):
        token = self.custom_user.microsoft_token
        if not token:
            return None

        headers = {
            'Authorization': f'Bearer {token.token}'
        }
        url = f"https://graph.microsoft.com/v1.0/me/drive/items/{self.folder_id}"

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get('name')  # The name of the folder
        else:
            return None
