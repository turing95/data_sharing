from copy import deepcopy

from django.db import models
from django.urls import reverse

from web_app.models import BaseModel, DeleteModel
from django.conf import settings
import pytz
import arrow


class Space(BaseModel, DeleteModel):
    TIMEZONE_CHOICES = tuple((tz, tz) for tz in pytz.all_timezones)

    title = models.CharField(max_length=250)
    user = models.ForeignKey('User', null=True, on_delete=models.SET_NULL, related_name='spaces')
    is_public = models.BooleanField(default=True)
    instructions = models.TextField(null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    upload_after_deadline = models.BooleanField(default=False)
    notify_deadline = models.BooleanField(default=False)
    notify_invitation = models.BooleanField(default=False)
    deadline_notice_days = models.PositiveSmallIntegerField(blank=True, null=True)
    deadline_notice_hours = models.PositiveSmallIntegerField(blank=True, null=True)
    timezone = models.CharField(
        max_length=50,
        choices=TIMEZONE_CHOICES
    )
    locale = models.CharField(max_length=10, null=True, blank=True, default='en-us')

    @property
    def link_for_email(self):
        return settings.BASE_URL + reverse('receiver_space_detail', kwargs={
            'space_uuid': self.uuid
        })
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

    def duplicate(self):

        new_space = deepcopy(self)
        new_space.pk = None
        new_space.title = f'{self.title} (copy)'
        new_space.save()
        for sender in self.senders.all():
            sender.duplicate(new_space)

        for request in self.requests.all():
            request.duplicate(new_space)
        return new_space
    @property
    def public_upload_events(self):
        return self.events.filter(sender__isnull=True)

    def get_deadline_url_ics(self, sender):
        # Format the deadline as YYYYMMDDTHHMMSSZ 
        if self.deadline is None:
            return None, None
        formatted_deadline = self.deadline.strftime('%Y%m%dT%H%M%SZ')

        '''# Calculate the reminder date (one day before the deadline)
        reminder_date = deadline - timedelta(days=self.deadline_reminder)
        formatted_reminder_date = reminder_date.strftime('%Y%m%dT%H%M%SZ')'''

        # Construct the calendar URL
        space_link = sender.full_space_link
        event_details = f"""You have been invited by: {self.user.email}<br><br>Go to Space: <a href="{space_link}">{self.title}</a>"""

        event_title = f"DEADLINE for upload space: {self.title}"

        ics_content = (
                "BEGIN:VCALENDAR\n"
                "VERSION:2.0\n"
                "PRODID:-//Your Company//Your Product//EN\n"
                "BEGIN:VEVENT\n"
                f"UID:{formatted_deadline}-space-{sender.uuid}@yourdomain.com\n"
                "DTSTAMP:" + formatted_deadline + "\n"
                                                  "DTSTART:" + formatted_deadline + "\n"
                                                                                    "DTEND:" + formatted_deadline + "\n"
                                                                                                                    f"SUMMARY:{event_title}\n"
                                                                                                                    f"DESCRIPTION:{event_details}\n"
                                                                                                                    "LOCATION:Online\n"
                                                                                                                    "END:VEVENT\n"
                                                                                                                    "END:VCALENDAR"
        )
        event_details = event_details.replace(' ', '+')
        event_title = event_title.replace(' ', '+')
        calendar_url = f'https://www.google.com/calendar/render?action=TEMPLATE&text={event_title}&dates={formatted_deadline}/{formatted_deadline}&details={event_details}&location=Online'
        return calendar_url, ics_content

    class Meta:
        ordering = ['-created_at']
