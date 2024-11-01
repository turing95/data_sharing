from web_app.models import BaseModel
from django.db import models
from web_app.storage_backends import PrivateMediaStorage
from django.utils.translation import gettext_lazy as _


class File(BaseModel):
    original_name = models.CharField(max_length=255)
    uid = models.CharField(max_length=255, default='noid')
    size = models.IntegerField()
    file_type = models.CharField(max_length=255)
    sender_event = models.ForeignKey('SenderEvent', on_delete=models.SET_NULL, related_name='files', null=True,
                                     blank=True)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='files', null=True)
    destination = models.ForeignKey('GenericDestination', on_delete=models.CASCADE, related_name='files', null=True)

    def __str__(self):
        return self.name

    @property
    def url(self):
        if self.destination is None:
            return None
        return self.destination.get_file_url(self.uid)

    @property
    def name(self):
        if self.destination is None:
            return None
        return self.destination.get_file_name(self.uid)

    @property
    def file(self):
        if self.destination is None:
            return None
        return self.destination.get_file(self.uid)
