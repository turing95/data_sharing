from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from web_app.models import Space


@login_required
@require_POST
def duplicate(request, space_uuid):
    Space.objects.get(pk=space_uuid).duplicate()
    return HttpResponseRedirect(reverse('spaces'))
