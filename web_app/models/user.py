import uuid

from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import AbstractUser
from django.core.mail import get_connection, EmailMultiAlternatives
from django.db import models
from django.template.loader import render_to_string
from django.utils.functional import cached_property
from django.utils.text import format_lazy
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from djstripe.models import Customer

from web_app.utils.drive_services import GoogleService, MicrosoftService
from utils.emails import html_to_text


class User(AbstractUser):
    '''
    Custom user model
    self.request.session['account_authentication_methods'] to access authentication methods( has social provider)
    '''
    organizations = models.ManyToManyField('Organization', through='UserOrganization')
    language = models.CharField(max_length=10, default='en')

    @property
    def full_name(self):
        return super().get_full_name()

    @property
    def can_create_space(self):
        if self.is_superuser:
            return True
        customer, _created = Customer.get_or_create(
            subscriber=self
        )
        if not customer.subscription and self.spaces.filter(
                is_deleted=False).count() >= settings.MAX_FREE_SPACES:
            return False
        return True

    @property
    def google_account(self):
        try:
            return SocialAccount.objects.get(user=self, provider='custom_google')
        except SocialAccount.DoesNotExist:
            return None

    @property
    def microsoft_account(self):
        try:
            return SocialAccount.objects.get(user=self, provider='custom_microsoft')
        except SocialAccount.DoesNotExist:
            return None

    def get_folders(self, destination_type, folder_name=None, sharepoint_site=None):
        from web_app.models import OneDrive, GoogleDrive, SharePoint
        if destination_type == GoogleDrive.TAG:
            return GoogleService(self.google_account).get_folders(folder_name)
        elif destination_type == OneDrive.TAG or destination_type == SharePoint.TAG:
            return MicrosoftService(self.microsoft_account).get_folders(folder_name, sharepoint_site)
        else:
            return None

    @cached_property
    def sharepoint_sites(self):
        if self.microsoft_account is None or self.microsoft_account.socialtoken_set.count() == 0:
            return None
        return MicrosoftService(self.microsoft_account).get_sites()

    def setup(self, request):
        from web_app.models import Organization, SenderNotificationsSettings, NotificationsSettings, \
            OrganizationInvitation
        SenderNotificationsSettings.objects.get_or_create(user=self)
        NotificationsSettings.objects.get_or_create(user=self)
        # Check if an organization named "Personal" already exists in the user's organizations
        personal_organization_exists = self.organizations.filter(name="Personal").exists()

        # If it does not exist, create it and add it to the user's organizations
        if not personal_organization_exists:
            personal_organization = Organization.objects.create(name="Personal", created_by=self)
            self.organizations.add(personal_organization)

        if request.session.get('invitation_uuid'):
            invitation = OrganizationInvitation.objects.get(pk=request.session['invitation_uuid'])
            invitation.organization.users.add(self)
            del request.session['invitation_uuid']
            invitation.delete()

    def notify_upload(self, sender_event):
        from web_app.models import NotificationsSettings
        from web_app.utils import get_base_context_for_email
        try:
            if sender_event.space.is_deleted is False and self.notifications_settings.on_sender_upload:
                context = get_base_context_for_email()
                pre_header_text_1 = _('New Upload to')
                pre_header_text_2 = _('in space')
                context['pre_header_text'] = format_lazy(
                    '{pre_header_text_1} {req_title} {pre_header_text_2} {space_title}',
                    pre_header_text_1=pre_header_text_1,
                    pre_header_text_2=pre_header_text_2,
                    space_title=sender_event.space.title,
                    req_title=sender_event.request.title
                )
                context['sender_event'] = sender_event

                email_html = render_to_string('emails/receiver_upload_notification.html', context)
                from_email = f"Kezyy <{settings.NO_REPLY_EMAIL}>"
                with get_connection(
                        host=settings.RESEND_SMTP_HOST,
                        port=settings.RESEND_SMTP_PORT,
                        username=settings.RESEND_SMTP_USERNAME,
                        password=settings.RESEND_API_KEY,
                        use_tls=True,
                ) as connection:
                    msg = EmailMultiAlternatives(
                        subject=context['pre_header_text'],
                        body=html_to_text(email_html),
                        from_email=from_email,
                        to=[self.email],
                        reply_to=[from_email],
                        connection=connection,
                        headers={'Return-Path': from_email}
                    )
                    msg.attach_alternative(email_html, 'text/html')

                    msg.send()
                return True
            return False
        except NotificationsSettings.DoesNotExist:
            NotificationsSettings.objects.create(user=self)
            return self.notify_upload(sender_event)
