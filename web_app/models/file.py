from web_app.models import BaseModel, SenderEvent
from django.db import models


class File(BaseModel):
    original_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    size = models.IntegerField()
    file_type = models.CharField(max_length=255)
    google_drive_url = models.CharField(max_length=255, null=True, blank=True)
    sender_event = models.ForeignKey('SenderEvent', on_delete=models.CASCADE, related_name='files')


class FileType(BaseModel):
    group = models.BooleanField(default=False)
    slug = models.CharField(max_length=50, unique=True)
    extension = models.CharField(max_length=50, null=True, blank=True)
    upload_requests = models.ManyToManyField('UploadRequest', through='UploadRequestFileType')
    group_type = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL,
                                   limit_choices_to={"group": True})

    @property
    def extensions(self):
        return [file_type.extension for file_type in self.filetype_set.all()]

    @property
    def formatted_extensions(self):
        return [file_type.formatted_extension for file_type in self.filetype_set.all()]

    @property
    def formatted_extension(self):
        if self.group is False:
            return f".{self.extension}"
        return None
