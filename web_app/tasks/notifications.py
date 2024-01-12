from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from utils.emails import html_to_text
from web_app import celery_app as app


@app.task
def sender_invite(sender_pk):
    from web_app.models import Sender
    sender = Sender.objects.get(pk=sender_pk)
    context = {
        'sender': sender,
    }
    calendar_url, ics_content = sender.space.get_deadline_url_ics(sender)

    context['calendar_url'] = calendar_url

    email_html = render_to_string('emails/sender_invite.html', context)
    from_email = 'marco1491995@gmail.com'  # TODO: change to config

    msg = EmailMultiAlternatives(
        subject='Invite to space',
        body=html_to_text(email_html),
        from_email=from_email,
        to=[sender.email],
        reply_to=[from_email],
        headers={'Return-Path': from_email}
    )
    msg.attach_alternative(email_html, 'text/html')
    if ics_content is not None:
        msg.attach('event.ics', ics_content, 'text/calendar')

    msg.send()


@app.task
def notify_deadline(sender_pk):
    return None
