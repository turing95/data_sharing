from django.views.generic import FormView
from web_app.mixins import SubscriptionMixin, GrantSideBarMixin, GrantMixin, GrantTabMixin
from django.urls import reverse
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
        kwargs['organization'] = self.get_grant().organization
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
