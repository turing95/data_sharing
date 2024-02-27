from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from djstripe.models import Customer
from djstripe.settings import djstripe_settings
from web_app.models import Space


@login_required
@require_POST
def duplicate(request, space_uuid):
    customer, _created = Customer.get_or_create(
        subscriber=djstripe_settings.subscriber_request_callback(request)
    )
    if not customer.subscription and request.user.spaces.filter(
            is_deleted=False).count() >= settings.MAX_FREE_SPACES:
        return redirect('create_checkout_session')
    space = get_object_or_404(Space, pk=space_uuid)
    space.duplicate(request.user)
    return HttpResponseRedirect(reverse('spaces'))
