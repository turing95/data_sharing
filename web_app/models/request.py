from django.db import models
from django.db.models import Q

from web_app.models import BaseModel, DeleteModel
import arrow


class UploadRequest(BaseModel, DeleteModel):
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
        '''constraints = [
            models.UniqueConstraint('title', 'space', name='unique_request_title')
        ]'''
        ordering = ['-created_at']

    @property
    def google_drive_destination(self):
        from web_app.models import GenericDestination, GoogleDrive
        generic_destination: GenericDestination = self.destinations.filter(tag=GoogleDrive.TAG, is_active=True).first()
        google_drive_destination: GoogleDrive = generic_destination.related_object
        return google_drive_destination

    @property
    def extensions(self):
        extensions = [file_type.extension for file_type in self.file_types.filter(group=False)]
        for file_type in self.file_types.filter(group=True):
            extensions += file_type.extensions
        return extensions

    @property
    def formatted_extensions(self):
        extensions = [file_type.formatted_extension for file_type in self.file_types.filter(group=False)]
        for file_type in self.file_types.filter(group=True):
            extensions += file_type.formatted_extensions
        return extensions

    def get_name_format_params(self, sender, original_file_name):
        format_params = {
            'upload_date': arrow.utcnow().date(),
            'original_file_name': original_file_name,
            'space_title': self.space.title,
            'request_title': self.title,
            'sender_email': sender.email if sender is not None else ''
        }
        return format_params

    def get_file_name_from_formula(self, sender, original_file_name):
        format_params = self.get_name_format_params(sender, original_file_name)
        if self.file_naming_formula is not None:
            file_name = self.file_naming_formula.format(**format_params)
        else:
            file_name = original_file_name
        return file_name


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


class UploadRequestFileType(BaseModel):
    upload_request = models.ForeignKey('UploadRequest', on_delete=models.CASCADE)
    file_type = models.ForeignKey('FileType', on_delete=models.CASCADE)
