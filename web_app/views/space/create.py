from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils import translation
from django.views.decorators.http import require_GET
from django.urls import reverse
from web_app.models import Space




@login_required
@require_GET
def space_create(request, organization_uuid):
    if not request.user.can_create_space:
        return redirect('create_checkout_session')
    space = Space.objects.create(title='untitled',
                                 user=request.user,
                                 organization_id=organization_uuid,
                                 locale=translation.get_language())
    return redirect(reverse('receiver_space_detail', kwargs={'space_uuid': space.pk}))
