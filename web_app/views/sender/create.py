from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET, require_POST
from web_app.forms import SenderCreateForm
from web_app.models import Space, Sender


@login_required
@require_GET
def sender_create_row(request, space_uuid):
    space = Space.objects.get(pk=space_uuid)
    sender = Sender.objects.create(space=space)
    form = SenderCreateForm(instance=sender, organization=space.organization)
    return render(request, 'private/space/detail/sender/sender_row.html',
                  {'space': space, 'organization': space.organization, 'sender': sender, 'form': form, })


@login_required
@require_POST
def sender_contact_update(request, sender_uuid):
    sender = get_object_or_404(Sender, pk=sender_uuid)
    
    form = SenderCreateForm(request.POST, instance=sender, organization=sender.space.organization)
    if form.is_valid():
        sender = form.save(commit=False)
        sender.save()
    return render(request, 'private/space/detail/sender/sender_row.html',
                    {'sender': sender})