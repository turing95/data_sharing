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
def get_count_uploaded_files(sender: Sender, upload_request: UploadRequest):
    return SenderEvent.objects.filter(sender=sender, request=upload_request).count()

@register.simple_tag
def get_list_of_uploaded_files_per_request(sender, upload_request):
    events = SenderEvent.objects.filter(sender=sender, request=upload_request, event_type=SenderEvent.EventType.FILE_UPLOADED)

    result = []
    for event in events:
        if event.file:
            timestamp = event.created_at
            formatted_date = timestamp.strftime("%Y-%m-%d")
            formatted_time = timestamp.strftime("%H:%M")
            result.append({'file': event.file, 'date': formatted_date, 'time': formatted_time})

    return result