from django.contrib.contenttypes.models import ContentType
from allauth.socialaccount.models import SocialAccount
from web_app.models import BaseModel
from django.db import models

from web_app.utils.drive_services import MicrosoftService


class OneDrive(BaseModel):
    TAG = 'one_drive'
    folder_id = models.CharField(max_length=255)
    user = models.ForeignKey('web_app.User', on_delete=models.CASCADE, null=True)
    social_account = models.ForeignKey(SocialAccount, on_delete=models.SET_NULL, null=True, blank=True)
    PROVIDER_ID = 'custom_microsoft'

    @classmethod
    def create_from_folder_id(cls, upload_request,space, folder_id, user):
        from web_app.models import GenericDestination
        one_drive_destination = cls(folder_id=folder_id, user=user, social_account=user.microsoft_account)

        generic_destination = GenericDestination(
            request=upload_request,
            space=space,
            content_type=ContentType.objects.get_for_model(cls),
            object_id=one_drive_destination.pk,
            social_account=user.microsoft_account,
            user=user,
            tag=cls.TAG,
        )

        generic_destination.save()
        one_drive_destination.save()

        return generic_destination

    @property
    def service(self):
        return MicrosoftService(self.social_account)

    def upload_file(self, file, file_name):
        return self.service.upload_file(file, file_name, self.folder_id).get('id', None)

    @property
    def url(self):
        return self.service.get_file_url(self.folder_id)

    @property
    def name(self):
        return self.service.get_file_name(self.folder_id)

    @property
    def alive(self):
        return self.service.is_file_alive(self.folder_id)

    def get_file_name(self, file_id):
        return self.service.get_file_name(file_id)

    def get_file_url(self, file_id):
        return self.service.get_file_url(file_id)

    def get_file(self, file_id):
        raise NotImplementedError