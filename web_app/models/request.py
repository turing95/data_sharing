from django.db import models
from web_app.models import BaseModel


class UploadRequest(BaseModel):
    class FileType(models.TextChoices):
        CSV = 'CSV', 'CSV'
        PDF = 'PDF', 'PDF'

    class FileNameTag(models.TextChoices):
        ORIGINAL_FILE_NAME = 'ORIGINAL_FILE_NAME', 'original file name'  # "The name with which the file is uploaded"
        SENDER_EMAIL = 'SENDER_EMAIL', 'sender email'  # "The email associated with the upload space link"
        UPLOAD_DATE = 'UPLOAD_DATE', 'upload date'  # "The date when the file was uploaded"
        SPACE_TITLE = 'SPACE_TITLE', 'space title'  # "The title of the space"
        REQUEST_TITLE = 'REQUEST_TITLE', 'request title'  # "The title of the request"
        
    #FILE_NAME_TAG_DESCRIPTIONS = #chaidi a chat. 

    space = models.ForeignKey('Space', on_delete=models.CASCADE, related_name='requests')
    title = models.CharField(max_length=50, null=True, blank=True)
    instructions = models.TextField(null=True, blank=True)
    file_name = models.CharField(max_length=255, null=True, blank=True)


class FileType(BaseModel):
    extension = models.CharField(max_length=50, unique=True)


class UploadRequestFileType(BaseModel):
    upload_request = models.ForeignKey('UploadRequest', on_delete=models.CASCADE, related_name='file_types')
    file_type = models.ForeignKey('FileType', on_delete=models.CASCADE, related_name='upload_requests')
