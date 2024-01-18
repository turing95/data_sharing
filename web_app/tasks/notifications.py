from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from utils.emails import html_to_text
from web_app import celery_app as app
from django.conf import settings


@app.task
def sender_invite(sender_pk):
    from web_app.models import Sender
    sender = Sender.objects.get(pk=sender_pk)
    sender.notify_invitation()


@app.task
def notify_deadline(sender_pk):
    from web_app.models import Sender
    sender = Sender.objects.get(pk=sender_pk)
    sender.notify_deadline()
