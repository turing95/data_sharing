import json

from django.core.mail import get_connection, EmailMultiAlternatives
from django.db import models
from django.template.loader import render_to_string
from django.templatetags.static import static

from data_sharing import settings
from utils.emails import html_to_text
from web_app.models import BaseModel, ActiveModel
import arrow
from django_celery_beat.models import PeriodicTask, ClockedSchedule
from django.urls import reverse


class Sender(BaseModel, ActiveModel):
    email = models.CharField(max_length=50)
    space = models.ForeignKey('Space', on_delete=models.CASCADE, related_name='senders')
    notified_at = models.DateTimeField(null=True, blank=True)
    invited_at = models.DateTimeField(null=True, blank=True)
    notification_task = models.ForeignKey(PeriodicTask, on_delete=models.SET_NULL, null=True, blank=True)

    def schedule_deadline_notification(self):
        if self.notification_task is not None:
            self.notification_task.delete()
        clocked, created = ClockedSchedule.objects.get_or_create(
            # Ensure that the datetime is timezone-aware and corresponds to the desired time
            clocked_time=self.space.deadline_notification_datetime
        )
        args = [str(self.pk)]
        task = PeriodicTask.objects.create(
            name='Deadline notification for sender {}'.format(self.pk),
            task='web_app.tasks.notifications.notify_deadline',
            args=json.dumps(args),
            kwargs={},
            clocked=clocked,  # Use the clocked schedule
            one_off=True
        )
        self.notification_task = task
        self.save()

    @property
    def full_space_link(self):
        return settings.BASE_URL + reverse('sender_space_detail_private', kwargs={
            'space_uuid': self.space.uuid,
            'sender_uuid': self.uuid
        })

    def notify_deadline(self):
        if self.is_active:
            context = {
                'pre_header_text': f'Remember to complete the upload for space: {self.space.title}',
                'sender': self,
                'contact_email': settings.CONTACT_EMAIL,
                'upload_requests': self.space.requests.filter(is_deleted=False).order_by('created_at'),
                'homepage_link': settings.BASE_URL,
                'logo_link': settings.BASE_URL + static('images/logo.png'),
                'space_link': self.full_space_link

            }
            email_html = render_to_string('emails/deadline_notification.html', context)
            from_email = f"Kezyy <{settings.NO_REPLY_EMAIL}>"
            with get_connection(
                    host=settings.RESEND_SMTP_HOST,
                    port=settings.RESEND_SMTP_PORT,
                    username=settings.RESEND_SMTP_USERNAME,
                    password=settings.RESEND_API_KEY,
                    use_tls=True,
            ) as connection:
                msg = EmailMultiAlternatives(
                    subject=f'Files upload reminder for space: {self.space.title}',
                    body=html_to_text(email_html),
                    from_email=from_email,
                    to=[self.email],
                    reply_to=[from_email],
                    connection=connection,
                    headers={'Return-Path': from_email}
                )
                msg.attach_alternative(email_html, 'text/html')

                msg.send()
            self.notified_at = arrow.utcnow().datetime
            self.save()
            return True
        return False

    def notify_invitation(self):
        context = {
            'pre_header_text': f'{self.space.user.email} invites you to upload files to the space: {self.space.title}',
            'sender': self,
            'contact_email': settings.CONTACT_EMAIL,
            'upload_requests': self.space.requests.filter(is_deleted=False).order_by('created_at'),
            'homepage_link': settings.BASE_URL,
            'logo_link': settings.BASE_URL + static('images/logo.png'),
            'space_link': self.full_space_link

        }
        calendar_url, ics_content = self.space.get_deadline_url_ics(self)

        context['calendar_url'] = calendar_url

        email_html = render_to_string('emails/sender_invite.html', context)
        from_email = f"Kezyy <{settings.NO_REPLY_EMAIL}>"
        with get_connection(
                host=settings.RESEND_SMTP_HOST,
                port=settings.RESEND_SMTP_PORT,
                username=settings.RESEND_SMTP_USERNAME,
                password=settings.RESEND_API_KEY,
                use_tls=True,
        ) as connection:
            msg = EmailMultiAlternatives(
                subject=f'Invitation to upload space: {self.space.title}',
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
        self.invited_at = arrow.utcnow().datetime
        self.save()
