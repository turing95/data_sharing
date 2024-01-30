from django.contrib import admin
from web_app.models import Sender, Space, UploadRequest, GoogleDrive, FileType,GenericDestination, UploadRequestFileType, SenderEvent, OneDrive,User
from django.contrib.auth.admin import UserAdmin

admin.site.register(User, UserAdmin)

@admin.register(Sender, Space, GoogleDrive, FileType, SenderEvent, OneDrive,GenericDestination)
class BaseAdmin(admin.ModelAdmin):
    pass


@admin.register(UploadRequestFileType)
class UploadRequestFileTypeAdmin(admin.ModelAdmin):
    search_fields = ['upload_request__uuid', 'upload_request__title', 'upload_request__space__uuid',
                     'file_type__extension']


@admin.register(UploadRequest)
class UploadRequestFileTypeAdmin(admin.ModelAdmin):
    search_fields = ['uuid', 'title', 'space__uuid']
