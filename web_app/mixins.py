import stripe
from django.shortcuts import get_object_or_404
from djstripe.mixins import PaymentsContextMixin
from djstripe.models import Plan, Customer, APIKey
from djstripe.settings import djstripe_settings
from django.conf import settings

from web_app.models import Organization


class SubscriptionMixin(PaymentsContextMixin):
    """Adds customer subscription context to a view."""

    def get_context_data(self, *args, **kwargs):
        if djstripe_settings.STRIPE_LIVE_MODE is True:
            stripe.api_key = APIKey.objects.get(name='STRIPE_LIVE_SECRET_KEY').secret
        else:
            stripe.api_key = APIKey.objects.get(name='STRIPE_TEST_SECRET_KEY').secret
        """Inject is_plans_plural and customer into context_data."""
        context = super().get_context_data(**kwargs)
        context["is_plans_plural"] = Plan.objects.count() > 1
        if self.request.user.is_authenticated:
            context["customer"], _created = Customer.get_or_create(
                subscriber=djstripe_settings.subscriber_request_callback(self.request)
            )
            context["subscription"] = context["customer"].subscription
            context['new_space_button_text'] = 'New space' if self.request.user.can_create_space is True else 'Upgrade to create more spaces'
        return context


class OrganizationMixin:
    _organization = None  # Placeholder for the cached object

    def get_organization(self) -> Organization:
        if self._organization is None:
            self._organization = get_object_or_404(Organization,
                                                   pk=self.kwargs.get('organization_uuid'),
                                                   users=self.request.user)
        return self._organization

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['organization'] = self.get_organization()
        return data


class SideBarMixin:
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['sidebar'] = True
        return data
