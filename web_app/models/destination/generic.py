from copy import deepcopy
from allauth.socialaccount.models import SocialAccount
from web_app.models import PolymorphicRelationModel, ActiveModel
from django.db import models


class GenericDestination(PolymorphicRelationModel, ActiveModel):
    tag = models.CharField(max_length=50)
    request = models.ForeignKey('UploadRequest', on_delete=models.SET_NULL, related_name='destinations', blank=True,
                                null=True)
    space = models.ForeignKey('Space', on_delete=models.SET_NULL, related_name='destinations', blank=True, null=True)
    social_account = models.ForeignKey(SocialAccount, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey('web_app.User', on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.tag

    def duplicate(self, request):
        new_destination = deepcopy(self)
        new_destination.pk = None
        new_destination.request = request
        new_destination.save()
        return new_destination

    @property
    def alive(self):
        return self.related_object.alive

    @property
    def folder_id(self):
        return self.related_object.folder_id

    @property
    def name(self):
        return self.related_object.name

    @property
    def url(self):
        return self.related_object.url

    def upload_file(self, file, file_name):
        return self.related_object.upload_file(file, file_name)

    @classmethod
    def create_provider(cls, destination_type, user=None, folder_id=None, sharepoint_site=None, request_instance=None,
                        space=None):
        from web_app.models import GoogleDrive, OneDrive, SharePoint, Kezyy
        if destination_type == GoogleDrive.TAG:
            return GoogleDrive.create_from_folder_id(request_instance, space, folder_id, user)
        elif destination_type == OneDrive.TAG:
            return OneDrive.create_from_folder_id(request_instance, space, folder_id, user)
        elif destination_type == SharePoint.TAG:
            return SharePoint.create_from_folder_id(request_instance, space, folder_id, user,
                                                    sharepoint_site)
        elif destination_type == Kezyy.TAG:
            return Kezyy.create(request_instance, space, user)
        else:
            raise NotImplementedError

    def get_file_url(self, file_id):
        return self.related_object.get_file_url(file_id)

    def get_file_name(self, file_id):
        return self.related_object.get_file_name(file_id)

    @classmethod
    def create_from_form(cls, request, form):
        cls.objects.filter(request=form.instance).update(is_active=False)
        cls.create_provider(
            form.cleaned_data.get('destination_type'),
            request.user,
            form.cleaned_data.get('destination_id'),
            form.cleaned_data.get('sharepoint_site_id'),
            request_instance=form.instance)
