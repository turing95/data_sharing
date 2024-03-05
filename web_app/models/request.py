from copy import deepcopy

from django.db import models
from utils.strings import fill_template
from web_app.models import BaseModel, ActiveModel
import arrow


class UploadRequest(BaseModel, ActiveModel):
    class FileNameTag(models.TextChoices):
        ORIGINAL_FILE_NAME = 'ORIGINAL_FILE_NAME', 'original_file_name'  # "The name with which the file is uploaded"
        SENDER_EMAIL = 'SENDER_EMAIL', 'sender_email'  # "The email associated with the upload space link"
        SENDER_COMPANY = 'SENDER_COMPANY', 'sender_company'  # "The email associated with the upload space link"
        SENDER_FULL_NAME = 'SENDER_FULL_NAME', 'sender_full_name'  # "The email associated with the upload space link"
        UPLOAD_DATE = 'UPLOAD_DATE', 'upload_date'  # "The date when the file was uploaded"
        SPACE_TITLE = 'SPACE_TITLE', 'space_title'  # "The title of the space"
        REQUEST_TITLE = 'REQUEST_TITLE', 'request_title'  # "The title of the request"

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
    def google_drive_destination(self):
        from web_app.models import GenericDestination, GoogleDrive
        generic_destination: GenericDestination = self.destinations.filter(tag=GoogleDrive.TAG, is_active=True).first()
        if generic_destination is None:
            return None
        google_drive_destination: GoogleDrive = generic_destination.related_object
        return google_drive_destination

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
        return UploadRequestForm(instance=self,user=self.request.space.user,prefix=self.uuid)




class TextRequest(BaseModel):
    label = models.CharField(max_length=50, null=True, blank=True)
    request = models.ForeignKey('Request', on_delete=models.CASCADE, related_name='text_requests')


class Request(BaseModel):
    space = models.ForeignKey('Space', on_delete=models.CASCADE, related_name='requests')
    title = models.CharField(max_length=50, null=True, blank=True)
    instructions = models.TextField(null=True, blank=True)


class InputRequest(BaseModel):
    upload_request = models.ForeignKey('UploadRequest', on_delete=models.CASCADE, null=True)
    text_request = models.ForeignKey('TextRequest', on_delete=models.CASCADE, null=True)
    request = models.ForeignKey('Request', on_delete=models.CASCADE, related_name='input_requests', null=True)
