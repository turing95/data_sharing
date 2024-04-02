from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.http import require_POST

from web_app.models import Grant

from django.views.generic import FormView
from web_app.mixins import SubscriptionMixin, GrantSideBarMixin, GrantMixin, GrantTabMixin
from web_app.forms import GrantForm
from django.contrib.auth.mixins import LoginRequiredMixin


class GrantEditView(LoginRequiredMixin, SubscriptionMixin, GrantSideBarMixin, GrantTabMixin, GrantMixin, FormView):
    template_name = "private/grant/edit.html"
    form_class = GrantForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grant_tab']['edit']['active'] = True
        return context

    # def get_success_url(self):
    #     return reverse('companies', kwargs={'organization_uuid': self.get_company().organization.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_grant()
        kwargs['organization'] = self.get_organization()
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


@login_required
@require_POST
def grant_update_name(request, grant_uuid):
    grant = Grant.objects.get(pk=grant_uuid)
    if request.method == 'POST':
        form = grant.name_form(request.POST)
        if form.is_valid():
            form.save()
        else:
            messages.error(request, form.errors['name'])
        return render(request, 'private/grant/grant_name.html',
                      {'form': grant.name_form(), 'from_htmx': True})
    return HttpResponseBadRequest()


@login_required
@require_POST
def grant_update(request, grant_uuid):
    grant = Grant.objects.get(pk=grant_uuid)
    if request.method == 'POST':
        form = grant.form(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'private/grant/grant_form.html',
                          {'form': grant.form()})
        return render(request, 'private/grant/grant_form.html',
                      {'form': form})
    return HttpResponseBadRequest()
