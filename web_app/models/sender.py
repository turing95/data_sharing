from django.db import models
from django.urls import reverse

from web_app.models import BaseModel, ActiveModel


class Sender(BaseModel, ActiveModel):
    email = models.CharField(max_length=50)
    space = models.ForeignKey('Space', on_delete=models.CASCADE, related_name='senders')

    @property
    def link(self):
        return reverse('sender_space_detail_private', kwargs={'space_uuid': self.space.uuid, 'sender_uuid': self.uuid})

    @property
    def requests(self):
        return self.space.requests.all()
