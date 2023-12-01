from django.contrib.contenttypes.models import ContentType

from web_app.models import PolymorphicRelationModel, BaseModel
from django.db import models


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
