from django.db import models
from web_app.models import BaseModel, ActiveModel


class Sender(BaseModel,ActiveModel):
    email = models.CharField(max_length=50)
    request = models.ForeignKey('Request', on_delete=models.CASCADE, related_name='senders')
