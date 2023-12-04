from django.db import models
from web_app.models import BaseModel, ActiveModel
from django.conf import settings


class Space(BaseModel,ActiveModel):
    title = models.CharField(max_length=250)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='spaces')
    is_public = models.BooleanField(default=True)
    instructions = models.TextField(null=True,blank=True)
    class Meta:
        constraints = [
            models.UniqueConstraint('user','title',name='unique_space_title')
        ]
