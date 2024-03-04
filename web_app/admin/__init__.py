from django.contrib import admin
from web_app.models import Sender, Space, UploadRequest, GoogleDrive, GenericDestination, SenderEvent, OneDrive, User, BetaAccessRequest, Organization, UserOrganization, \
    SenderNotificationsSettings, Contact
from django.contrib.auth.admin import UserAdmin

admin.site.register(User, UserAdmin)


@admin.register(Sender, Space, GoogleDrive, SenderEvent, OneDrive, GenericDestination, BetaAccessRequest,SenderNotificationsSettings,Contact)
class BaseAdmin(admin.ModelAdmin):
    pass


@admin.register(UploadRequest)
class UploadRequestAdmin(admin.ModelAdmin):
    search_fields = ['uuid', 'title', 'space__uuid']


class UserOrganizationInline(admin.TabularInline):
    model = UserOrganization
    extra = 1


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    inlines = (UserOrganizationInline,)
