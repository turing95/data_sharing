from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_POST

from web_app.forms.widgets import ToggleWidget
from web_app.models import Sender


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
                                            'hx-trigger': 'click', 'hx-swap': 'outerHTML','hx-target':'closest .cursor-pointer'})
    )


@login_required
@require_POST
def notify_sender(request, sender_uuid):
    sender = Sender.objects.get(pk=sender_uuid)
    sender.notify_deadline()
    messages.success(request, f"Sender {sender.email} notified")
    return render(
        request,
        'components/messages.html'
    )
