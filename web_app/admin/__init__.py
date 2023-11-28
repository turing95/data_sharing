from django.contrib import admin
from web_app.models import Sender,Space,UploadRequest, GoogleDrive


@admin.register(Sender, Space,UploadRequest, GoogleDrive)
class BaseAdmin(admin.ModelAdmin):
    pass
