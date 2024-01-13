import logging
import stripe
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views.decorators.http import require_GET
from djstripe import models
from djstripe import settings as djstripe_settings
from djstripe.models import APIKey
from stripe import api_key

logger = logging.getLogger(__name__)

User = get_user_model()
stripe.api_key = APIKey.objects.get(name='STRIPE_TEST_SECRET_KEY').secret


@login_required
@require_GET
def create_checkout_session(request):
    """
            Creates and returns a Stripe Checkout Session
            """
    # Get Parent Context

    success_url = request.build_absolute_uri(
        reverse("generic_home")
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

    try:
        # retreive the Stripe Customer.
        customer = models.Customer.objects.get(subscriber=request.user)

        print("Customer Object in DB.")

        # ! Note that Stripe will always create a new Customer Object if customer id not provided
        # ! even if customer_email is provided!
        session = stripe.checkout.Session.create(
            customer=customer.id,
            line_items=[
                {
                    "price": "price_1OU7F0Fp43jm0b8rXRzNw9y6",
                    "quantity": 1,
                },
            ],
            mode="subscription",
            success_url=success_url,
            cancel_url=cancel_url,
            metadata=metadata,
        )

    except models.Customer.DoesNotExist:
        print("Customer Object not in DB.")

        session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price": "price_1OU7F0Fp43jm0b8rXRzNw9y6",
                    "quantity": 1,
                },
            ],
            mode="subscription",
            success_url=success_url,
            cancel_url=cancel_url,
            metadata=metadata,
        )

    return redirect(session.url, code=303)
