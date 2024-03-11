from web_app.models import BaseModel
from django.db import models


class Grant(BaseModel):
    name = models.CharField(max_length=250, null=True, blank=True)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='grants')
