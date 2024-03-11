from copy import deepcopy
from django.contrib.contenttypes.models import ContentType
from web_app.models import BaseModel
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from web_app.storage_backends import PrivateMediaStorage


class Kezyy(BaseModel):
    TAG = 'kezyy'
    user = models.ForeignKey('web_app.User', on_delete=models.CASCADE, null=True)
    generic_destination = GenericRelation('GenericDestination')

    @classmethod
    def create(cls, upload_request,space, user):
        from web_app.models import GenericDestination
        kezyy_destination = cls(user=user)

        generic_destination = GenericDestination(
            request=upload_request,
            space=space,
            content_type=ContentType.objects.get_for_model(cls),
            object_id=kezyy_destination.pk,
            user=user,
            tag=cls.TAG,
        )

        generic_destination.save()
        kezyy_destination.save()

        return generic_destination

    def upload_file(self, file, file_name):
        from web_app.models import KezyyFile
        file = deepcopy(file)
        file.name = file_name
        kezyy_file = KezyyFile.objects.create(upload=file, destination=self)
        return kezyy_file.upload.name

    @property
    def folder_id(self):
        return None

    @property
    def url(self):
        return None

    @property
    def name(self):
        return 'Kezyy'

    @property
    def alive(self):
        return True

    def get_file_name(self, file_id):
        from web_app.models import KezyyFile
        return KezyyFile.objects.get(upload=file_id).upload.name

    def get_file_url(self, file_id):
        return KezyyFile.objects.get(upload=file_id).upload.url


class KezyyFile(BaseModel):
    destination = models.ForeignKey('Kezyy', on_delete=models.CASCADE, related_name='files')
    file = models.OneToOneField('File', on_delete=models.CASCADE, related_name='kezyy_file', null=True, blank=True)
    upload = models.FileField(storage=PrivateMediaStorage())
