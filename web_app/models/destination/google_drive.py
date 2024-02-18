from django.contrib.contenttypes.models import ContentType
from allauth.socialaccount.models import SocialAccount
from web_app.models import BaseModel
from django.db import models
from web_app.utils.drive_services import GoogleService


class GoogleDrive(BaseModel):
    TAG = 'google_drive'
    folder_id = models.CharField(max_length=255)
    user = models.ForeignKey('web_app.User', on_delete=models.CASCADE, null=True)
    social_account = models.ForeignKey(SocialAccount, on_delete=models.SET_NULL, null=True, blank=True)
    PROVIDER_ID = 'custom_google'

    @classmethod
    def create_from_folder_id(cls, upload_request, folder_id, user):
        from web_app.models import GenericDestination
        google_drive_destination = cls(folder_id=folder_id, user=user, social_account=user.google_account)

        generic_destination = GenericDestination(
            request=upload_request,
            content_type=ContentType.objects.get_for_model(cls),
            object_id=google_drive_destination.pk,
            social_account=user.google_account,
            tag=cls.TAG,
        )

        generic_destination.save()
        google_drive_destination.save()

        return generic_destination

    @property
    def service(self):
        return GoogleService(self.social_account)

    @property
    def alive(self):
        return self.service.is_file_alive(self.folder_id)

    @property
    def name(self):
        return self.service.get_file_name(self.folder_id)

    @property
    def url(self):
        return self.service.get_file_url(self.folder_id)

    def upload_file(self, file, file_name):
        return self.service.upload_file(file, file_name, self.folder_id).get('id', None)

    def get_file_name(self, file_id):
        return self.service.get_file_name(file_id)

    def get_file_url(self, file_id):
        return self.service.get_file_url(file_id)
