from django.db import models
from web_app.models import BaseModel, ActiveModel
from django.conf import settings
import pytz


class Space(BaseModel, ActiveModel):
    TIMEZONE_CHOICES = tuple((tz, tz) for tz in pytz.all_timezones)

    title = models.CharField(max_length=250)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name='spaces')
    is_public = models.BooleanField(default=True)
    instructions = models.TextField(null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    timezone = models.CharField(
        max_length=50,
        choices=TIMEZONE_CHOICES
    )
    
    @property
    def upload_events(self):
        from web_app.models import SenderEvent
        return SenderEvent.objects.filter(request__space=self, event_type=SenderEvent.EventType.FILE_UPLOADED)

    @property
    def public_upload_events(self):
        return self.upload_events.filter(sender__isnull=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint('user', 'title', name='unique_space_title')
        ]
        ordering = ['-created_at']
