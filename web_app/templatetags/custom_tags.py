from django import template
from django.urls import reverse

from web_app.forms.widgets import SenderToggle
from web_app.models import Sender, SenderEvent, UploadRequest, File
from web_app.forms.widgets.toggle import ToggleWidget

register = template.Library()


@register.filter(name='split')
def split(value, key):
    """
        Returns the value turned into a list.
    """
    return value.split(key)


@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)


@register.filter(name='get_message_color')
def get_message_color(value):
    colors = {
        "success": "green",
        "error": "red",
        "warning": "yellow",
        "info": "blue"
    }
    return colors.get(value, "blue")


@register.simple_tag
def get_count_uploaded_files(upload_request: UploadRequest, sender: Sender = None, public=False):
    files = File.objects.filter(sender_event__request=upload_request)
    if sender:
        files = files.filter(sender_event__sender=sender)
    elif public:
        files = files.filter(sender_event__sender=None)
    return files.count()


@register.simple_tag
def get_list_of_upload_events_per_request(sender, upload_request):
    events = SenderEvent.objects.filter(sender=sender, request=upload_request,
                                        event_type=SenderEvent.EventType.FILE_UPLOADED)

    return events


@register.inclusion_tag("forms/widgets/toggle.html")
def render_sender_activate_toggle(sender, name, value, **kwargs):
    return SenderToggle(**kwargs).get_context(name, value,
                                              {'hx-post': reverse('toggle_sender_active',
                                                                  kwargs={'sender_uuid': sender.pk}),
                                               'hx-trigger': f"click", 'hx-swap': 'none', 'sender-uuid': sender.pk})


@register.inclusion_tag("forms/widgets/toggle.html")
def render_space_public_link_toggle(space, name, value):
    return ToggleWidget(label_on='Public link', label_off='Public link').get_context(name, value,
                                                                                     {
                                                                                         'hx-post': reverse(
                                                                                             'toggle_space_public',
                                                                                             kwargs={
                                                                                                 'space_uuid': space.pk}),
                                                                                         'hx-swap': 'morph:outerHTML'})


@register.inclusion_tag("forms/widgets/toggle.html")
def render_sender_notification_activate_toggle(request):
    return ToggleWidget(label_on='Get receipt', label_off='Get receipt').get_context('sender_upload_notification', request.session.get('sender_upload_notification',False),
                                                                                     {
                                                                                         'hx-params':'sender_upload_notification',
                                                                                         'hx-post': reverse(
                                                                                             'sender_upload_notification'),'hx-swap': 'none'})
