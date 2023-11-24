from django.db import models
from web_app.models import BaseModel


class Space(BaseModel):
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_public = models.BooleanField(default=True)
