from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST

from web_app.forms import SenderNotificationsSettingsForm


@login_required
@require_POST
def sender_notifications_settings(request, *args, **kwargs):
    form = SenderNotificationsSettingsForm(request.POST or None, instance=request.user.sender_notifications_settings)
    if form.is_valid():
        messages.success(request, "Settings updated")
        form.save()
    return render(request, "private/settings/notifications_form.html", {"form": form, 'from_htmx': True})
