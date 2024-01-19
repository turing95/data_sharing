from django.db import models
from web_app.models import BaseModel, ActiveModel, DeleteModel
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
import pytz
from datetime import timedelta
import arrow
from decimal import Decimal


class Space(BaseModel,DeleteModel):
    TIMEZONE_CHOICES = tuple((tz, tz) for tz in pytz.all_timezones)

    title = models.CharField(max_length=250)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name='spaces')
    is_public = models.BooleanField(default=True)
    instructions = models.TextField(null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    upload_after_deadline = models.BooleanField(default=False)
    notify_deadline = models.BooleanField(default=False)
    notify_invitation = models.BooleanField(default=False)
    deadline_notice_days = models.PositiveSmallIntegerField(blank=True,null=True)
    deadline_notice_hours = models.PositiveSmallIntegerField(blank=True,null=True)
    timezone = models.CharField(
        max_length=50,
        choices=TIMEZONE_CHOICES
    )
    locale = models.CharField(max_length=10, null=True, blank=True,default='en-us')

    @property
    def deadline_notification_datetime(self):
        if not self.deadline or self.deadline_notice_days is None or self.deadline_notice_hours is None:
            return None
        notice_days = self.deadline_notice_days or 0
        notice_hours = self.deadline_notice_hours or 0


        # Calculate notification datetime in the server timezone
        notification_dt = arrow.get(self.deadline).shift(days=-notice_days, hours=-notice_hours)
        return notification_dt.datetime
    
    @property
    def deadline_expired(self):
        return bool(self.deadline) and self.deadline < arrow.utcnow()
    
    @property
    def upload_events(self):
        from web_app.models import SenderEvent
        return SenderEvent.objects.filter(
            request__space=self,
            event_type=SenderEvent.EventType.FILE_UPLOADED
            ).select_related('sender').prefetch_related('request', 'request__destinations')
        
    @property
    def public_upload_events(self):
        return self.upload_events.filter(sender__isnull=True)

    def get_deadline_url_ics(self, sender):
        # Format the deadline as YYYYMMDDTHHMMSSZ
        if self.deadline is None or self.notify_deadline is False:
            return None, None
        deadline = self.deadline
        formatted_deadline = deadline.strftime('%Y%m%dT%H%M%SZ')

        '''# Calculate the reminder date (one day before the deadline)
        reminder_date = deadline - timedelta(days=self.deadline_reminder)
        formatted_reminder_date = reminder_date.strftime('%Y%m%dT%H%M%SZ')'''

        # Construct the calendar URL
        calendar_url = f'https://www.google.com/calendar/render?action=TEMPLATE&text=Reminder:+Deadline+for+{self.title}&dates={formatted_deadline}/{formatted_deadline}&details=Deadline+Reminder&location=Online'
        ics_content = (
                "BEGIN:VCALENDAR\n"
                "VERSION:2.0\n"
                "PRODID:-//Your Company//Your Product//EN\n"
                "BEGIN:VEVENT\n"
                f"UID:{formatted_deadline}-space-{sender.uuid}@yourdomain.com\n"
                "DTSTAMP:" + formatted_deadline + "\n"
                                                  "DTSTART:" + formatted_deadline + "\n"
                                                                                         "DTEND:" + formatted_deadline + "\n"
                                                                                                                         f"SUMMARY:Reminder: Deadline for {self.title}\n"
                                                                                                                         "DESCRIPTION:Deadline Reminder\n"
                                                                                                                         "LOCATION:Online\n"
                                                                                                                         "END:VEVENT\n"
                                                                                                                         "END:VCALENDAR"
        )
        return calendar_url, ics_content

    class Meta:
        ordering = ['-created_at']
