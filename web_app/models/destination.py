from django.contrib.contenttypes.models import ContentType

from web_app.models import PolymorphicRelationModel, BaseModel,ActiveModel
from django.db import models
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from io import BytesIO


class GenericDestination(PolymorphicRelationModel,ActiveModel):
    tag = models.CharField(max_length=50)
    request = models.ForeignKey('UploadRequest', on_delete=models.CASCADE, related_name='destinations')

    def __str__(self):
        return self.tag


class GoogleDrive(BaseModel):
    TAG = 'GOOGLE_DRIVE'
    folder_id = models.CharField(max_length=255)

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
        file = self.service.files().get(supportsAllDrives=True,  fileId=self.folder_id,
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
        file = self.service.files().create(supportsAllDrives=True,body=file_metadata,
                                           media_body=media,
                                           fields='id').execute()
        return file

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
