import logging
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
def create_billing_session(request):
    if djstripe_settings.djstripe_settings.STRIPE_LIVE_MODE is True:
        stripe.api_key = APIKey.objects.get(name='STRIPE_LIVE_SECRET_KEY').secret
    else:
        stripe.api_key = APIKey.objects.get(name='STRIPE_TEST_SECRET_KEY').secret

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
