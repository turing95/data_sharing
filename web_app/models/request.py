from copy import deepcopy

from django.db import models
from django.db.models import Max

from utils.strings import fill_template
from web_app.models import BaseModel, ActiveModel
import arrow


class UploadRequest(BaseModel):
    class FileNameTag(models.TextChoices):
        ORIGINAL_FILE_NAME = 'ORIGINAL_FILE_NAME', 'original_file_name'  # "The name with which the file is uploaded"
        SENDER_EMAIL = 'SENDER_EMAIL', 'sender_email'  # "The email associated with the upload space link"
        SENDER_COMPANY = 'SENDER_COMPANY', 'sender_company'  # "The email associated with the upload space link"
        SENDER_FULL_NAME = 'SENDER_FULL_NAME', 'sender_full_name'  # "The email associated with the upload space link"
        UPLOAD_DATE = 'UPLOAD_DATE', 'upload_date'  # "The date when the file was uploaded"
        SPACE_TITLE = 'SPACE_TITLE', 'space_title'  # "The title of the space"
        REQUEST_TITLE = 'REQUEST_TITLE', 'request_title'  # "The title of the request"

    title = models.CharField(max_length=250, null=True, blank=True)
    instructions = models.TextField(null=True, blank=True)
    request = models.ForeignKey('Request', on_delete=models.CASCADE, related_name='upload_requests', null=True)
    file_naming_formula = models.CharField(max_length=255, null=True, blank=True)
    file_template = models.URLField(null=True, blank=True)
    multiple_files = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def duplicate(self, space):
        new_request = deepcopy(self)
        new_request.pk = None
        new_request.space = space
        new_request.save()
        for destination in self.destinations.all():
            destination.duplicate(new_request)
        return new_request

    @property
    def destination(self):
        destination = self.destinations.filter(is_active=True).order_by('-created_at').first()
        if destination is None:
            destination = self.destinations.order_by('-created_at').first()
        return destination

    @property
    def active_destination(self):
        destination = self.destinations.filter(is_active=True).order_by('-created_at').first()
        return destination

    def get_name_format_params(self, sender, original_file_name):

        format_params = {
            'upload_date': arrow.utcnow().format('YYYY-MM-DD', locale=self.request.space.locale),
            'original_file_name': original_file_name,
            'space_title': self.request.space.title,
            'request_title': self.request.title,
            'sender_email': sender.email if sender is not None else '',
            'sender_company': sender.company if sender is not None else '',
            'sender_full_name': sender.full_name if sender is not None else '',
        }
        return format_params

    def get_file_name_from_formula(self, sender, original_file_name):
        format_params = self.get_name_format_params(sender, original_file_name)
        if self.file_naming_formula is not None:
            file_name = fill_template(self.file_naming_formula, format_params)
        else:
            file_name = original_file_name
        return file_name

    def request_form(self):
        from web_app.forms import UploadRequestForm
        return UploadRequestForm(instance=self, user=self.request.space.user, prefix=self.uuid)

    @property
    def outputs(self):
        from web_app.models import Output
        return Output.objects.filter(sender_event__upload_request=self)

    @property
    def last_output(self):
        return self.outputs.order_by('-created_at').first()


class TextRequest(BaseModel):
    title = models.CharField(max_length=250, null=True, blank=True)
    instructions = models.TextField(null=True, blank=True)
    request = models.ForeignKey('Request', on_delete=models.CASCADE, related_name='text_requests')

    def request_form(self):
        from web_app.forms import TextRequestForm
        return TextRequestForm(instance=self, prefix=self.uuid)

    @property
    def outputs(self):
        from web_app.models import Output
        return Output.objects.filter(sender_event__text_request=self)

    @property
    def last_output(self):
        return self.outputs.order_by('-created_at').first()


class Request(BaseModel, ActiveModel):
    space = models.ForeignKey('Space', on_delete=models.CASCADE, related_name='requests')
    title = models.CharField(max_length=250, null=True, blank=True)
    instructions = models.TextField(null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    upload_after_deadline = models.BooleanField(default=False)
    notify_deadline = models.BooleanField(default=False)
    deadline_notice_days = models.PositiveSmallIntegerField(blank=True, null=True)
    deadline_notice_hours = models.PositiveSmallIntegerField(blank=True, null=True)

    def add_input_request(self, space_request, text_request=None, upload_request=None, prev_request_position=None):
        from web_app.models import InputRequest
        if prev_request_position:
            inserting_position = int(prev_request_position) + 1
        else:
            inserting_position = 1
        # increase by 1 all the positions of the input requests that have a position greater than or equal to the inserting position
        self.input_requests.filter(position__gte=inserting_position).update(
            position=models.F('position') + 1)
        input_request = InputRequest.objects.create(request=space_request, upload_request=upload_request,
                                                    text_request=text_request,
                                                    position=inserting_position)
        
    
    @property
    def latest_event_date(self):
        from django.db.models import Max
        events = self.events
        latest_event_date = events.aggregate(Max('created_at'))['created_at__max']
        return latest_event_date

    @property
    def input_requests_position_sorted(self):
        return self.input_requests.order_by('position')

    @property
    def completed_input_requests(self):
        return self.input_requests.filter(is_complete=True)

    @property
    def is_complete(self):
        return self.input_requests.filter(is_complete=False).count() == 0

    def title_form(self, request_post=None):
        from web_app.forms import RequestTitleForm
        return RequestTitleForm(request_post, instance=self)

    def instructions_form(self, request_post=None):
        from web_app.forms import RequestEditForm
        return RequestEditForm(request_post, instance=self)

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

    def get_deadline_url_ics(self, sender):
        # Format the deadline as YYYYMMDDTHHMMSSZ
        if self.deadline is None:
            return None, None
        formatted_deadline = self.deadline.strftime('%Y%m%dT%H%M%SZ')

        '''# Calculate the reminder date (one day before the deadline)
        reminder_date = deadline - timedelta(days=self.deadline_reminder)
        formatted_reminder_date = reminder_date.strftime('%Y%m%dT%H%M%SZ')'''

        # Construct the calendar URL
        space_link = sender.link_for_email
        event_details = f"""You have been invited by: {self.space.user.email}<br><br>Go to Space: <a href="{space_link}">{self.title}</a>"""

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


class InputRequest(BaseModel):
    upload_request = models.OneToOneField('UploadRequest', on_delete=models.CASCADE, null=True,
                                          related_name='input_request')
    text_request = models.OneToOneField('TextRequest', on_delete=models.CASCADE, null=True,
                                        related_name='input_request')
    request = models.ForeignKey('Request', on_delete=models.CASCADE, related_name='input_requests', null=True)
    position = models.PositiveIntegerField(default=1)
    is_complete = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
