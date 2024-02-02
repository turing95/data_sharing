from djstripe import webhooks
from djstripe.models import Subscription,Event


@webhooks.handler("invoice.payment_failed")
def custom_webhook(event, **kwargs):
    try:
        Subscription.objects.get(id=event.data['object']['subscription']).cancel()
    except Subscription.DoesNotExist:
        print('subscription not found')
