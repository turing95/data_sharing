import json
from copy import deepcopy

from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _
from django.core.mail import get_connection, EmailMultiAlternatives
from django.db import models
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.utils.translation import activate, get_language

from data_sharing import settings
from utils.emails import html_to_text
from web_app.models import BaseModel, ActiveModel
import arrow
from django_celery_beat.models import PeriodicTask, ClockedSchedule
from django.urls import reverse


class Sender(BaseModel, ActiveModel):
    email = models.CharField(max_length=50)
    contact = models.ForeignKey('Contact', on_delete=models.CASCADE, related_name='senders', null=True)
    space = models.ForeignKey('Space', on_delete=models.CASCADE, related_name='senders')
    notified_at = models.DateTimeField(null=True, blank=True)
    invited_at = models.DateTimeField(null=True, blank=True)
    notification_task = models.ForeignKey(PeriodicTask, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def company(self):
        return self.contact.company or ''

    @property
    def full_name(self):
        return f'{self.contact.first_name} {self.contact.last_name}'

    def duplicate(self, space):
        new_sender = deepcopy(self)
        new_sender.pk = None
        new_sender.space = space
        new_sender.notification_task = None
        new_sender.save()
        return new_sender

    def schedule_deadline_notification(self):
        if self.notification_task is not None:
            self.notification_task.delete()
        clocked, created = ClockedSchedule.objects.get_or_create(
            # Ensure that the datetime is timezone-aware and corresponds to the desired time
            clocked_time=self.space.deadline_notification_datetime
        )
        args = [str(self.pk)]
        task = PeriodicTask.objects.create(
            name=_('Deadline notification for sender {}').format(self.pk),
            task='web_app.tasks.notifications.notify_deadline',
            args=json.dumps(args),
            kwargs={},
            clocked=clocked,  # Use the clocked schedule
            one_off=True
        )
        self.notification_task = task
        self.save()

    @property
    def link_for_email(self):
        return settings.BASE_URL + reverse('sender_space_detail_private', kwargs={
            'space_uuid': self.space.uuid,
            'sender_uuid': self.uuid
        })

    def get_context_for_email(self):
        from web_app.utils import get_base_context_for_email
        context = get_base_context_for_email()
        ctx_update = {
            'sender': self,
            'receiver_email': self.space.user.sender_notifications_settings.reference_email,
            'receiver_name': self.space.user.sender_notifications_settings.name or self.space.user.sender_notifications_settings.reference_email,
            'upload_requests': self.space.requests.filter(is_active=True).order_by('created_at'),
            'space_link': self.link_for_email

        }
        context.update(ctx_update)
        return context

    def notify_deadline(self):
        current_language = get_language()  # Store the current language
        try:
            if self.is_active and self.space.is_deleted is False:
                activate(self.space.user.sender_notifications_settings.language)
                context = self.get_context_for_email()
                pre_header_text = _('Remember to complete the upload to the space:')
                context['pre_header_text'] = format_lazy('{pre_header_text} {title}', pre_header_text=pre_header_text,
                                                         title=self.space.title)
                title_text = _('Upload reminder for the space:')
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
                        subject=format_lazy('{title_text} {title}', title_text=title_text, title=self.space.title),
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
        finally:
            activate(current_language)  # Restore the original language

    def notify_invitation(self):
        current_language = get_language()  # Store the current language
        try:
            if self.is_active and self.space.is_deleted is False:
                activate(self.space.user.sender_notifications_settings.language)
                context = self.get_context_for_email()
                pre_header_text = _('invites you to upload files to the space:')
                invitation_title_text = _('Invitation:')
                context['pre_header_text'] = format_lazy('{receiver_name} {pre_header_text} {title}',
                                                         receiver_name=context["receiver_name"],
                                                         pre_header_text=pre_header_text,
                                                         title=self.space.title)
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
                        subject=format_lazy('{invitation_title_text} {receiver_name} {pre_header_text} {title}',
                                            invitation_title_text=invitation_title_text,
                                            pre_header_text=pre_header_text,
                                            receiver_name=context["receiver_name"],
                                            title=self.space.title),
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
                return True
            return False
        finally:
            activate(current_language)  # Restore the original language

    def notify_changes_request(self, upload_request, files, notes):
        current_language = get_language()  # Store the current language
        try:
            if self.is_active and self.space.is_deleted is False:
                activate(self.space.user.sender_notifications_settings.language)
                context = self.get_context_for_email()
                context[
                    'pre_header_text'] = _(f'{context["receiver_name"]} has requested changes for {upload_request.title}')
                pre_header_text = _('has requested changes for')
                changes_title_text = _('Changes Requested:')
                context['pre_header_text'] = format_lazy('{receiver_name} {pre_header_text} {title}',
                                                         receiver_name=context["receiver_name"],
                                                         pre_header_text=pre_header_text,
                                                         title=upload_request.title)
                context['notes'] = notes
                context['upload_request'] = upload_request
                context['files'] = files

                email_html = render_to_string('emails/changes_notification.html', context)
                from_email = f"Kezyy <{settings.NO_REPLY_EMAIL}>"
                with get_connection(
                        host=settings.RESEND_SMTP_HOST,
                        port=settings.RESEND_SMTP_PORT,
                        username=settings.RESEND_SMTP_USERNAME,
                        password=settings.RESEND_API_KEY,
                        use_tls=True,
                ) as connection:
                    msg = EmailMultiAlternatives(
                        subject=format_lazy('{changes_title_text} {receiver_name} {pre_header_text} {title}',
                                            changes_title_text=changes_title_text,
                                            pre_header_text=pre_header_text,
                                            receiver_name=context["receiver_name"],
                                            title=self.space.title),
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
        finally:
            activate(current_language)  # Restore the original language

    def notify_upload(self, sender_event):
        current_language = get_language()  # Store the current language
        try:
            if self.is_active and self.space.is_deleted is False:
                activate(self.space.user.sender_notifications_settings.language)
                context = self.get_context_for_email()
                context[
                    'pre_header_text'] = _('Your Upload receipt')
                context['sender_event'] = sender_event

                email_html = render_to_string('emails/sender_upload_notification.html', context)
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
        finally:
            activate(current_language)  # Restore the original language
