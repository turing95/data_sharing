from django.db import models
from web_app.models import BaseModel
from django.conf import settings
import pytz


class UserSettings(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, related_name='settings')

    # Timezone choices
    TIMEZONE_CHOICES = tuple((tz, tz) for tz in pytz.all_timezones)

    # Timezone field
    timezone = models.CharField(
        max_length=50,
        choices=TIMEZONE_CHOICES
    )
