from web_app.models import BaseModel
from django.db import models


class File(BaseModel):
    original_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    size = models.IntegerField()
    file_type = models.CharField(max_length=255)
