from django.contrib import admin
from web_app.models import Sender,Space


@admin.register(Sender, Space)
class BaseAdmin(admin.ModelAdmin):
    pass
