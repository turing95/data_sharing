import logging
import stripe
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.http import require_GET
from djstripe import models
from djstripe.settings import djstripe_settings
from djstripe.models import APIKey, Product

logger = logging.getLogger(__name__)


@login_required
@require_GET
def create_billing_session(request):
    stripe.api_key = djstripe_settings.STRIPE_SECRET_KEY

    return_url = request.build_absolute_uri(reverse("generic_home"))

    try:
        # retreive the Stripe Customer.
        customer = models.Customer.objects.get(subscriber=request.user)
        session = stripe.billing_portal.Session.create(
            customer=customer.id,
            return_url=return_url,
        )

    except models.Customer.DoesNotExist:
        session = stripe.billing_portal.Session.create(
            return_url=return_url
        )

    return redirect(session.url, code=303)
