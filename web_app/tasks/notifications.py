from web_app import celery_app as app


@app.task
def notify_invitation(sender_pk):
    from web_app.models import Sender
    sender = Sender.objects.get(pk=sender_pk)
    sender.notify_invitation()


@app.task
def notify_deadline(sender_pk):
    from web_app.models import Sender
    sender = Sender.objects.get(pk=sender_pk)
    sender.notify_deadline()
