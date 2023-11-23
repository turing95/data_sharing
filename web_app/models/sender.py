from django.db import models
from web_app.models import BaseModel


class Sender(BaseModel):
    email = models.CharField(max_length=50)
    space = models.ForeignKey('Space', on_delete=models.CASCADE, related_name='senders')
    is_active = models.BooleanField(default=True)

