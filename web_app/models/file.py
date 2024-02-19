from web_app.models import BaseModel
from django.db import models
from web_app.storage_backends import PrivateMediaStorage


class File(BaseModel):
    class FileStatus(models.TextChoices):
        ACCEPTED = 'Accepted', 'Accepted'
        REJECTED = 'Rejected', 'Rejected'
        PENDING = 'Pending', 'Pending'

    original_name = models.CharField(max_length=255)
    uid = models.CharField(max_length=255,default='noid')
    size = models.IntegerField()
    file_type = models.CharField(max_length=255)
    sender_event = models.ForeignKey('SenderEvent', on_delete=models.CASCADE, related_name='files')
    destination = models.ForeignKey('GenericDestination', on_delete=models.CASCADE, related_name='files',null=True)
    status = models.CharField(
        max_length=50,
        choices=FileStatus.choices,
        default=FileStatus.PENDING,
    )

    def __str__(self):
        return self.name

    @property
    def url(self):
        if self.destination is None:
            return None
        return self.destination.get_file_url(self.uid)

    @property
    def name(self):
        if self.destination is None:
            return None
        return self.destination.get_file_name(self.uid)


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
