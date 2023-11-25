from django.contrib import admin
from web_app.models import Sender,Space,Request


@admin.register(Sender, Space,Request)
class BaseAdmin(admin.ModelAdmin):
    pass
