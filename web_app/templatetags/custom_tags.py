from django import template
from web_app.models import Sender, SenderEvent, UploadRequest, File

register = template.Library()


@register.filter(name='split')
def split(value, key):
    """
        Returns the value turned into a list.
    """
    return value.split(key)


@register.simple_tag
def get_count_uploaded_files(upload_request: UploadRequest, sender: Sender = None):
        return SenderEvent.objects.filter(sender=sender, request=upload_request).count()

@register.simple_tag
def get_list_of_upload_events_per_request(sender, upload_request):
    events = SenderEvent.objects.filter(sender=sender, request=upload_request,
                                        event_type=SenderEvent.EventType.FILE_UPLOADED)

    return events
