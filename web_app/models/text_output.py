from web_app.models import BaseModel
from django.db import models


class TextOutput(BaseModel):

    sender_event = models.ForeignKey('SenderEvent', on_delete=models.CASCADE, related_name='text_outputs', null=True,
                                     blank=True)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='text_outputs', null=True)
    text = models.TextField(null=True, blank=True)
