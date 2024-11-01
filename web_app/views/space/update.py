from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from web_app.models import Space
from django.utils.translation import gettext_lazy as _


@login_required
@require_POST
def space_update(request, space_uuid):
    space = get_object_or_404(Space, pk=space_uuid)
    if request.method == 'POST':
        form = space.title_form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Space saved'))
            return render(request, 'private/space/detail/space_title_form.html',
                          {'from_htmx': True, 'form': space.title_form(), 'space': space})
        messages.error(request, form.errors)
        return render(request, 'private/space/detail/space_title_form.html',
                      {'from_htmx': True, 'form': space.title_form(), 'space': space})
    return HttpResponseBadRequest()
