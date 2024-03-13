from django.db import models
from web_app.models import BaseModel


class SenderEvent(BaseModel):
    class EventType(models.TextChoices):
        FILE_UPLOADED = 'FILE_UPLOADED', 'File uploaded'
        TEXT_CREATED = 'TEXT_CREATED', 'Text created'

    sender = models.ForeignKey('Sender', on_delete=models.CASCADE, related_name='events',null=True)
    request = models.ForeignKey('Request', on_delete=models.SET_NULL, related_name='events',null=True)
    upload_request = models.ForeignKey('UploadRequest', on_delete=models.SET_NULL, related_name='events',null=True)
    text_request = models.ForeignKey('TextRequest', on_delete=models.SET_NULL, related_name='events',null=True)
    destination = models.ForeignKey('GenericDestination', on_delete=models.SET_NULL, related_name='events',null=True)
    space = models.ForeignKey('Space', on_delete=models.SET_NULL, related_name='events',null=True)
    event_type = models.CharField(max_length=100, choices=EventType.choices)
    notes = models.TextField(null=True, blank=True)

    def notify(self, notify_sender=False):
        if notify_sender:
            self.sender.notify_upload(self)
        self.space.user.notify_upload(self)
