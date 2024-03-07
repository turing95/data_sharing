from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from web_app.forms import SenderCreateForm
from web_app.models import Space


@login_required
@require_GET
def sender_create_row(request, space_uuid):
    space = Space.objects.get(pk=space_uuid)
    form = SenderCreateForm(organization=space.organization)
    return render(request, 'private/space/detail/sender/sender_row.html',
                  {'create_sender': True, 'space': space, 'organization': space.organization, 'form': form})


@login_required
@require_POST
def sender_create(request, space_uuid):
    space = Space.objects.get(pk=space_uuid)
    form = SenderCreateForm(request.POST, organization=space.organization)
    if form.is_valid():
        sender = form.save(commit=False)
        sender.space = space
        sender.save()
        return render(request, 'private/space/detail/sender/sender_row.html',
                      {'sender': sender, 'space': space, 'organization': space.organization})
    return render(request, 'private/space/detail/sender/sender_row.html',
                  {'create_sender': True, 'space': space, 'organization': space.organization, 'form': form})
