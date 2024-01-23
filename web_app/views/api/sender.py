from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_POST, require_GET

from web_app.forms.widgets import ToggleWidget
from web_app.models import Sender, Space
from web_app.tasks.notifications import notify_deadline as notify_deadline_task, \
    notify_invitation as notify_invitation_task


@login_required
@require_POST
def toggle_sender_active(request, sender_uuid):
    sender = Sender.objects.get(pk=sender_uuid)
    sender.is_active = not sender.is_active
    sender.save()
    return render(
        request,
        "forms/widgets/toggle.html",
        ToggleWidget(color_on="green",
                     color_off="orange",
                     toggle_color_on="marian-blue",
                     toggle_color_off="gray",
                     label_on="active",
                     label_off="inactive",
                     soft_off_label=False,
                     label_colored=True,
                     label_wrap=True).get_context('sender_toggle', sender.is_active,
                                                  {'hx-post': reverse('toggle_sender_active',
                                                                      kwargs={'sender_uuid': sender.pk}),
                                                   'hx-trigger': 'click', 'hx-swap': 'outerHTML',
                                                   'hx-target': 'closest .cursor-pointer'})
    )


@login_required
@require_POST
def notify_deadline(request, sender_uuid):
    sender = Sender.objects.get(pk=sender_uuid)
    #notify_deadline_task.delay(sender.pk)
    sender.notify_deadline()
    messages.success(request, f"{sender.email} notified")
    return render(
        request,
        'components/messages.html'
    )


@login_required
@require_POST
def notify_invitation(request, sender_uuid):
    sender = Sender.objects.get(pk=sender_uuid)
    #notify_invitation_task.delay(sender.pk)
    sender.notify_invitation()
    messages.success(request, f"{sender.email} invited")
    return render(
        request,
        'components/messages.html'
    )


@login_required
@require_GET
def sender_modal(request, sender_uuid):
    sender = Sender.objects.get(pk=sender_uuid)

    return render(request, 'private/space/detail/components/sender_modal.html',
                  {'sender': sender})


@login_required
@require_GET
def sender_info(request, sender_uuid):
    sender = Sender.objects.get(pk=sender_uuid)

    return render(request, 'private/space/detail/components/sender_info.html',
                  {'sender': sender})


@login_required
@require_GET
def sender_row(request, sender_uuid):
    sender = Sender.objects.get(pk=sender_uuid)

    return render(request, 'private/space/detail/components/sender_row.html',
                  {'sender': sender})
