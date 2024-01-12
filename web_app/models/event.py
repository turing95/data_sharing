from django.db import models
from web_app.models import BaseModel


class SenderEvent(BaseModel):
    class EventType(models.TextChoices):
        FILE_UPLOADED = 'FILE_UPLOADED', 'File uploaded'

    sender = models.ForeignKey('Sender', on_delete=models.CASCADE, related_name='events',null=True)
    request = models.ForeignKey('UploadRequest', on_delete=models.CASCADE, related_name='events')
    event_type = models.CharField(max_length=100, choices=EventType.choices)
