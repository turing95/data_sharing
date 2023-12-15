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


@register.inclusion_tag("forms/widgets/toggle.html")
def build_toggle(**kwargs):
    """ to render a toggle button in a template"""
    # Define default values for the keys
    defaults = {
        'color_on': 'blue',
        'color_off': 'gray',
        'label_on': '',
        'label_off': '',
        'label_colored': False,
        'soft_off_label': False,
        'label_wrap': False,
        'label_wrap_mono': False
    }

    # Update defaults with provided kwargs
    defaults.update(kwargs)

    return defaults