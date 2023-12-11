from django.contrib import admin
from web_app.models import Sender,Space,UploadRequest, GoogleDrive,FileType,UploadRequestFileType, SenderEvent


@admin.register(Sender, Space,UploadRequest, GoogleDrive,FileType, SenderEvent)
class BaseAdmin(admin.ModelAdmin):
    pass
@admin.register(UploadRequestFileType)
class UploadRequestFileTypeAdmin(admin.ModelAdmin):
    search_fields = ['upload_request__uuid','upload_request__title','upload_request__space__uuid', 'file_type__extension']