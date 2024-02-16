from django.db import models
from web_app.models import BaseModel
from django.conf import settings
import pytz


class SenderNotificationsSettings(BaseModel):
    user = models.OneToOneField('User', on_delete=models.CASCADE,
                                related_name='sender_notifications_settings')
    name = models.CharField(max_length=100, null=True)
    reference_email = models.EmailField(null=True)
    language = models.CharField(max_length=10, default=settings.LANGUAGE_CODE)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.user.full_name
        if not self.reference_email:
            self.reference_email = self.user.email
        super().save(*args, **kwargs)



class NotificationsSettings(BaseModel):
    user = models.OneToOneField('User', on_delete=models.CASCADE,
                                related_name='notifications_settings')
    on_sender_upload = models.BooleanField(default=False)
