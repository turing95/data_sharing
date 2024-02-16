import smtplib

from web_app import celery_app as app


@app.task(autoretry_for=(smtplib.SMTPServerDisconnected,),
          retry_kwargs={'max_retries': 5}, default_retry_delay=5)
def notify_invitation(sender_pk):
    from web_app.models import Sender
    sender = Sender.objects.get(pk=sender_pk)
    sender.notify_invitation()


@app.task(autoretry_for=(smtplib.SMTPServerDisconnected,),
          retry_kwargs={'max_retries': 5}, default_retry_delay=5)
def notify_deadline(sender_pk):
    from web_app.models import Sender
    sender = Sender.objects.get(pk=sender_pk)
    sender.notify_deadline()


@app.task(autoretry_for=(smtplib.SMTPServerDisconnected,),
          retry_kwargs={'max_retries': 5}, default_retry_delay=5)
def notify_beta_access_request(req_pk):
    from web_app.models import BetaAccessRequest
    req = BetaAccessRequest.objects.get(pk=req_pk)
    return req.notify()


@app.task(autoretry_for=(smtplib.SMTPServerDisconnected,),
          retry_kwargs={'max_retries': 5}, default_retry_delay=5)
def bulk_notify_invitation(space_pk):
    from web_app.models import Space
    space = Space.objects.get(pk=space_pk)
    for sender in space.senders.all():
        sender.notify_invitation()


@app.task(autoretry_for=(smtplib.SMTPServerDisconnected,),
          retry_kwargs={'max_retries': 5}, default_retry_delay=5)
def bulk_notify_deadline(space_pk):
    from web_app.models import Space
    space = Space.objects.get(pk=space_pk)
    for sender in space.senders.all():
        sender.notify_deadline()


@app.task(autoretry_for=(smtplib.SMTPServerDisconnected,),
          retry_kwargs={'max_retries': 5}, default_retry_delay=5)
def handle_sender_upload(sender_event_pk, notify_sender=False):
    from web_app.models import SenderEvent
    sender_event = SenderEvent.objects.get(pk=sender_event_pk)
    sender_event.notify(notify_sender=notify_sender)
