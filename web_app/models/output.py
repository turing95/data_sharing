from web_app.models import BaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class Output(BaseModel):
    class OutputStatus(models.TextChoices):
        ACCEPTED = 'Accepted', _('Accepted')
        REJECTED = 'Rejected', _('Rejected')
        PENDING = 'Pending', _('Pending')

    sender_event = models.ForeignKey('SenderEvent', on_delete=models.CASCADE, related_name='outputs', null=True,
                                     blank=True)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='outputs', null=True)
    status = models.CharField(
        max_length=50,
        choices=OutputStatus.choices,
        default=OutputStatus.PENDING,
    )
    text_output = models.OneToOneField('TextOutput', on_delete=models.CASCADE, related_name='output', null=True,
                                       blank=True)
    file = models.OneToOneField('File', on_delete=models.CASCADE, related_name='file', null=True, blank=True)

    @property
    def content(self):
        if self.text_output:
            return self.text_output.text
        elif self.file:
            return self.file.name
        return None

    @property
    def update_event(self):
        return f'outputUpdated-{self.pk}'

    def reject_form(self,request_post=None):
        from web_app.forms import OutputRejectForm
        return OutputRejectForm(request_post)