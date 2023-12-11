from django.db import models
from web_app.models import BaseModel


class UploadRequest(BaseModel):
    class FileType(models.TextChoices):
        CSV = 'CSV', 'CSV'
        PDF = 'PDF', 'PDF'

    class FileNameTag(models.TextChoices):
        ORIGINAL_FILE_NAME = 'ORIGINAL_FILE_NAME', 'original_file_name'  # "The name with which the file is uploaded"
        SENDER_EMAIL = 'SENDER_EMAIL', 'sender_email'  # "The email associated with the upload space link"
        UPLOAD_DATE = 'UPLOAD_DATE', 'upload_date'  # "The date when the file was uploaded"
        SPACE_TITLE = 'SPACE_TITLE', 'space_title'  # "The title of the space"
        REQUEST_TITLE = 'REQUEST_TITLE', 'request_title'  # "The title of the request"

    space = models.ForeignKey('Space', on_delete=models.CASCADE, related_name='requests')
    title = models.CharField(max_length=50, null=True, blank=True)
    instructions = models.TextField(null=True, blank=True)
    file_naming_formula = models.CharField(max_length=255, null=True, blank=True)
    file_types = models.ManyToManyField('FileType', through='UploadRequestFileType')

    class Meta:
        constraints = [
            models.UniqueConstraint('title', 'space', name='unique_request_title')
        ]
        ordering = ['-created_at']

    @property
    def google_drive_destination(self):
        from web_app.models import GenericDestination, GoogleDrive
        generic_destination: GenericDestination = self.destinations.filter(tag=GoogleDrive.TAG).first()
        google_drive_destination: GoogleDrive = generic_destination.related_object
        return google_drive_destination


class FileType(BaseModel):
    extension = models.CharField(max_length=50, unique=True)
    upload_requests = models.ManyToManyField('UploadRequest', through='UploadRequestFileType')


class UploadRequestFileType(BaseModel):
    upload_request = models.ForeignKey('UploadRequest', on_delete=models.CASCADE)
    file_type = models.ForeignKey('FileType', on_delete=models.CASCADE)
