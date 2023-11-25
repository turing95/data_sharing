from django.db import models
from web_app.models import BaseModel, ActiveModel
from django.conf import settings


class Space(BaseModel,ActiveModel):
    name = models.CharField(max_length=50)
    deadline = models.DateTimeField()  # TODO  deadline model missing
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='spaces')
    is_public = models.BooleanField(default=True)
