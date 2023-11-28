from django.db import models
from web_app.models import BaseModel


class UploadRequest(BaseModel):
    class FileType(models.TextChoices):
        CSV = 'CSV', 'CSV'
        PDF = 'PDF', 'PDF'

    space = models.ForeignKey('Space', on_delete=models.CASCADE, related_name='requests')
    file_number = models.IntegerField(null=True, blank=True)
    file_type = models.CharField(max_length=50, null=True, blank=True)
    max_file_size = models.IntegerField(null=True, blank=True)
