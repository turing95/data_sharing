from web_app.models import PolymorphicRelationModel, BaseModel
from django.db import models
from django.conf import settings


class GenericDestination(PolymorphicRelationModel):
    tag = models.CharField(max_length=50)

    def __str__(self):
        return self.tag


class GoogleDrive(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='gdrive_folders')
    folder_id = models.CharField(max_length=255)
