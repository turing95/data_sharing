import logging

import arrow
import stripe
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.http import require_GET
from djstripe import models
from djstripe import settings as djstripe_settings
from djstripe.models import APIKey, Product

logger = logging.getLogger(__name__)


@login_required
@require_GET
def create_checkout_session(request):
    if djstripe_settings.djstripe_settings.STRIPE_LIVE_MODE is True:
        stripe.api_key = APIKey.objects.get(name='STRIPE_LIVE_SECRET_KEY').secret
    else:
        stripe.api_key = APIKey.objects.get(name='STRIPE_TEST_SECRET_KEY').secret

    success_url = request.build_absolute_uri(
        reverse("spaces")
    )
    cancel_url = request.build_absolute_uri(reverse("generic_home"))

    # get the id of the Model instance of djstripe_settings.djstripe_settings.get_subscriber_model()
    # here we have assumed it is the Django User model. It could be a Team, Company model too.
    # note that it needs to have an email field.
    _id = request.user.id

    # example of how to insert the SUBSCRIBER_CUSTOMER_KEY: id in the metadata
    # to add customer.subscriber to the newly created/updated customer.
    metadata = {
        f"{djstripe_settings.djstripe_settings.SUBSCRIBER_CUSTOMER_KEY}": _id
    }
    line_items = [
        {
            "price": Product.objects.get(name="Kezyy Pro").default_price.id,
            "quantity": 1,
        },
    ]
    try:
        # retreive the Stripe Customer.
        customer = models.Customer.objects.get(subscriber=request.user)
        # ! Note that Stripe will always create a new Customer Object if customer id not provided
        # ! even if customer_email is provided!
        session = stripe.checkout.Session.create(
            customer=customer.id,
            line_items=line_items,
            billing_address_collection='auto',
            customer_update={'address': 'auto'},
            automatic_tax={'enabled': True},
            mode="subscription",
            success_url=success_url,
            cancel_url=cancel_url,
            metadata=metadata,

        )


    except models.Customer.DoesNotExist:
        print("Customer Object not in DB.")

        session = stripe.checkout.Session.create(
            line_items=line_items,
            mode="subscription",
            success_url=success_url,
            cancel_url=cancel_url,
            metadata=metadata,
        )

    return redirect(session.url, code=303)
