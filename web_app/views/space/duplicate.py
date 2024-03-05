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
    if not request.user.can_create_space:
        return redirect('create_checkout_session')
    space = get_object_or_404(Space, pk=space_uuid)
    space.duplicate(request.user)
    return HttpResponseRedirect(reverse('spaces'))
