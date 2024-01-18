from django.core.mail import get_connection, EmailMultiAlternatives
from django.db import models
from django.template.loader import render_to_string
from data_sharing import settings
from utils.emails import html_to_text
from web_app.models import BaseModel, ActiveModel


class Sender(BaseModel, ActiveModel):
    email = models.CharField(max_length=50)
    space = models.ForeignKey('Space', on_delete=models.CASCADE, related_name='senders')

    def notify_deadline(self):
        context = {
            'sender': self,
        }
        email_html = render_to_string('emails/deadline_notification.html', context)
        from_email = settings.NO_REPLY_EMAIL
        with get_connection(
                host=settings.RESEND_SMTP_HOST,
                port=settings.RESEND_SMTP_PORT,
                username=settings.RESEND_SMTP_USERNAME,
                password=settings.RESEND_API_KEY,
                use_tls=True,
        ) as connection:
            msg = EmailMultiAlternatives(
                subject='Deadline notification',
                body=html_to_text(email_html),
                from_email=from_email,
                to=[self.email],
                reply_to=[from_email],
                connection=connection,
                headers={'Return-Path': from_email}
            )
            msg.attach_alternative(email_html, 'text/html')

            msg.send()

    def notify_invitation(self):
        context = {
            'sender': self,
        }
        calendar_url, ics_content = self.space.get_deadline_url_ics(self)

        context['calendar_url'] = calendar_url

        email_html = render_to_string('emails/sender_invite.html', context)
        from_email = settings.NO_REPLY_EMAIL
        with get_connection(
                host=settings.RESEND_SMTP_HOST,
                port=settings.RESEND_SMTP_PORT,
                username=settings.RESEND_SMTP_USERNAME,
                password=settings.RESEND_API_KEY,
                use_tls=True,
        ) as connection:
            msg = EmailMultiAlternatives(
                subject='Invite to space',
                body=html_to_text(email_html),
                from_email=from_email,
                to=[self.email],
                reply_to=[from_email],
                connection=connection,
                headers={'Return-Path': from_email}
            )
            msg.attach_alternative(email_html, 'text/html')
            if ics_content is not None:
                msg.attach('event.ics', ics_content, 'text/calendar')

            msg.send()
