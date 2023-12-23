from django.db import models
from web_app.models import BaseModel, ActiveModel, DeleteModel
from django.conf import settings
import pytz


class Space(BaseModel, ActiveModel,DeleteModel):
    TIMEZONE_CHOICES = tuple((tz, tz) for tz in pytz.all_timezones)

    title = models.CharField(max_length=250)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name='spaces')
    is_public = models.BooleanField(default=True)
    instructions = models.TextField(null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    notify_deadline = models.BooleanField(default=False)
    timezone = models.CharField(
        max_length=50,
        choices=TIMEZONE_CHOICES
    )

    @property
    def upload_events(self):
        from web_app.models import SenderEvent
        return SenderEvent.objects.filter(
            request__space=self,
            event_type=SenderEvent.EventType.FILE_UPLOADED
        ).select_related('sender').prefetch_related('request', 'request__destinations')
    
    def get_filtered_upload_events(self, request_uuid=None, sender_uuid=None):
        events = self.upload_events 

        if request_uuid:
            events = events.filter(request__uuid=request_uuid)
        
        if sender_uuid:
            events = events.filter(sender__uuid=sender_uuid)

        return events 

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
        constraints = [
            models.UniqueConstraint('user', 'title', name='unique_space_title')
        ]
        ordering = ['-created_at']
