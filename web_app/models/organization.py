import uuid

from django.conf import settings
from django.core.mail import get_connection, EmailMultiAlternatives
from django.db import models, transaction
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _

from utils.emails import html_to_text
from web_app.models import BaseModel


class Organization(BaseModel):
    name = models.CharField(max_length=50)
    users = models.ManyToManyField('User', through='UserOrganization')
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='created_organizations', null=True)

    def invite_user(self, email, inviter):
        from web_app.utils import get_base_context_for_email
        from web_app.models import OrganizationInvitation
        with transaction.atomic():
            invitation = OrganizationInvitation.objects.create(email=email, organization=self, invited_by=inviter)
            context = get_base_context_for_email()
            pre_header_text_1 = _('wants you to join')
            pre_header_text_2 = _('Accept invitation')
            context['pre_header_text'] = format_lazy(
                '{user_identifier} {pre_header_text_1} {name}! {pre_header_text_2}',
                pre_header_text_1=pre_header_text_1,
                user_identifier=inviter.full_name or inviter.email,
                name=self.name,
                pre_header_text_2=pre_header_text_2)
            context['invitation'] = invitation
            context['user_identifier'] = inviter.full_name or inviter.email
            email_html = render_to_string('emails/team_invitation.html', context)
            from_email = f"Kezyy <{settings.NO_REPLY_EMAIL}>"
            with get_connection(
                    host=settings.RESEND_SMTP_HOST,
                    port=settings.RESEND_SMTP_PORT,
                    username=settings.RESEND_SMTP_USERNAME,
                    password=settings.RESEND_API_KEY,
                    use_tls=True,
            ) as connection:
                msg = EmailMultiAlternatives(
                    subject=format_lazy('{user_identifier} {pre_header_text_1} {name}!',
                                        user_identifier=inviter.full_name or inviter.email,
                                        pre_header_text_1=pre_header_text_1,
                                        name=inviter.full_name or inviter.email),
                    body=html_to_text(email_html),
                    from_email=from_email,
                    to=[email],
                    reply_to=[from_email],
                    connection=connection,
                    headers={'Return-Path': from_email}
                )
                msg.attach_alternative(email_html, 'text/html')
                msg.send()

    def notify_upload(self, sender_events):
        for user in self.users.all():
            user.notify_upload(sender_events)


class UserOrganization(BaseModel):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)


class OrganizationInvitation(BaseModel):
    email = models.EmailField()
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='invitations')
    invited_by = models.ForeignKey('User', on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)  # remove
    token = models.UUIDField(default=uuid.uuid4, editable=False)

    @property
    def link_for_email(self):
        return settings.BASE_URL + reverse('team_invitation_redemption') + f'?token={self.token}'
