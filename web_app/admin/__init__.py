from django.contrib import admin
from web_app.models import Sender,Space,UploadRequest, GoogleDrive,FileType


@admin.register(Sender, Space,UploadRequest, GoogleDrive,FileType)
class BaseAdmin(admin.ModelAdmin):
    pass
