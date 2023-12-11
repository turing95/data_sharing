from django.contrib.contenttypes.models import ContentType

from web_app.models import PolymorphicRelationModel, BaseModel
from django.db import models
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2.credentials import Credentials
from io import BytesIO


class GenericDestination(PolymorphicRelationModel):
    tag = models.CharField(max_length=50)
    request = models.ForeignKey('UploadRequest', on_delete=models.CASCADE)

    def __str__(self):
        return self.tag


class GoogleDrive(BaseModel):
    TAG = 'GOOGLE_DRIVE'
    folder_id = models.CharField(max_length=255)
    token = models.CharField(max_length=255)

    @classmethod
    def create_from_folder_id(cls, upload_request, folder_id, token):
        google_drive_destination = cls(folder_id=folder_id, token=token)

        generic_destination = GenericDestination(
            request=upload_request,
            content_type=ContentType.objects.get_for_model(cls),
            object_id=google_drive_destination.pk,
            tag=cls.TAG,
        )

        generic_destination.save()
        google_drive_destination.save()

        return generic_destination

    @staticmethod
    def get_credentials(access_token):
        credentials = Credentials(token=access_token)
        return credentials

    def get_service(self, access_token=None):
        return build('drive', 'v3', credentials=self.get_credentials(access_token=access_token))

    def get_name(self, access_token):
        print(access_token)
        service = self.get_service(access_token=access_token)
        file = service.files().get(fileId=self.folder_id,
                                   fields='name').execute()
        return file.get('name')

    def upload_file(self, file, file_name):
        service = self.get_service()

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
        file = service.files().create(body=file_metadata,
                                      media_body=media,
                                      fields='id').execute()
        return file
