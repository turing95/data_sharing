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
