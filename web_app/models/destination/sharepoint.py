from django.contrib.contenttypes.models import ContentType
from allauth.socialaccount.models import SocialAccount
from web_app.models import BaseModel
from django.db import models
from web_app.utils.drive_services import MicrosoftService


class SharePoint(BaseModel):
    TAG = 'sharepoint'
    folder_id = models.CharField(max_length=255)
    site_id = models.CharField(max_length=255)
    user = models.ForeignKey('web_app.User', on_delete=models.CASCADE, null=True)
    social_account = models.ForeignKey(SocialAccount, on_delete=models.SET_NULL, null=True, blank=True)
    PROVIDER_ID = 'custom_microsoft'

    @classmethod
    def create_from_folder_id(cls, upload_request, folder_id, user, site_id):
        from web_app.models import GenericDestination

        sharepoint_destination = cls(folder_id=folder_id, site_id=site_id, user=user,
                                     social_account=user.microsoft_account)

        generic_destination = GenericDestination(
            request=upload_request,
            content_type=ContentType.objects.get_for_model(cls),
            object_id=sharepoint_destination.pk,
            social_account=user.microsoft_account,
            tag=cls.TAG,
        )

        generic_destination.save()
        sharepoint_destination.save()

        return generic_destination

    @property
    def service(self):
        return MicrosoftService(self.social_account)

    def upload_file(self, file, file_name):
        return self.service.upload_file(file, file_name, self.folder_id, self.site_id)

    @property
    def url(self):
        return self.service.get_file_url(self.folder_id, self.site_id)

    @property
    def name(self):
        return self.service.get_file_name(self.folder_id, self.site_id)

    @property
    def alive(self):
        return self.service.is_file_alive(self.folder_id, self.site_id)
