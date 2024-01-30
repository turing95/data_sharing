from django.db import models

from web_app.models import BaseModel


class Organization(BaseModel):
    name = models.CharField(max_length=50)
