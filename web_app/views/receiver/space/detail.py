from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.utils.translation import gettext_lazy as _

from web_app.forms import SpaceForm, SpaceUpdateForm
from web_app.mixins import SubscriptionMixin, SpaceMixin, SpaceSideBarMixin
from web_app.models import Space, Contact, Sender
from web_app.tasks.notifications import notify_invitation



class SpaceDetailView(LoginRequiredMixin, SubscriptionMixin, SpaceMixin, SpaceSideBarMixin, TemplateView):
    template_name = "private/space/detail/base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['space'] = self.get_space()
        context['status'] = self.request.GET.get('status')
        context['space_summary'] = True
        context['form'] = SpaceUpdateForm(instance=self.get_space())
        return context


class SpaceSettingsView(LoginRequiredMixin, SubscriptionMixin, SpaceMixin, SpaceSideBarMixin, FormView):
    template_name = "private/space/detail/settings.html"
    form_class = SpaceForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['space'] = self.get_space()
        context['space_form'] = True
        context['submit_text'] = _('Save space')
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            space_instance = form.save(commit=False)
            space_instance.user = request.user
            space_instance.save()
            self.handle_senders(form.cleaned_data.get('senders_emails', []), space_instance)
            return self.form_valid(form)
        return self.form_invalid(form)

    def get_success_url(self):
        return self.request.path  # to summary page

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_space()
        kwargs['organization'] = self.get_space().organization
        return kwargs

    def handle_senders(self, senders_emails, space_instance: Space):

        existing_senders = {sender.email: sender for sender in space_instance.senders.filter(is_active=True)}

        # Add or update senders
        for email in senders_emails:
            email = email.strip()
            if email in existing_senders:
                del existing_senders[email]
            else:
                contact, created = Contact.objects.get_or_create(email=email, user=self.request.user)
                sender, created = Sender.objects.update_or_create(email=contact.email, contact=contact,
                                                                  space=space_instance, defaults={'is_active': True})
                if space_instance.notify_invitation is True:
                    notify_invitation.delay(sender.pk)

        # Delete removed emails
        for email, sender in existing_senders.items():
            if sender.events.exists():
                sender.is_active = False
                sender.save()
            else:
                sender.delete()
        for sender in space_instance.senders.all():
            if space_instance.deadline_notification_datetime is not None:
                sender.schedule_deadline_notification()
