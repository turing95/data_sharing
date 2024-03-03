from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.utils.translation import gettext_lazy as _

from web_app.forms import UserForm


@login_required
@require_POST
def profile(request, *args, **kwargs):
    form = UserForm(request.POST or None, instance=request.user)
    if form.is_valid():
        messages.success(request, _("Profile updated"))
        form.save()
    return render(request, "private/settings/profile_form.html", {"form": form,'from_htmx':True})
