import json

from django.core.mail import get_connection, EmailMultiAlternatives
from django.db import models
from django.template.loader import render_to_string
from data_sharing import settings
from utils.emails import html_to_text
from web_app.models import BaseModel, ActiveModel
import arrow
from django_celery_beat.models import PeriodicTask, ClockedSchedule


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

    def notify_deadline(self):
        if self.is_active:
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
            self.notified_at = arrow.utcnow().datetime
            self.save()
            return True
        return False

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
        self.invited_at = arrow.utcnow().datetime
        self.save()
