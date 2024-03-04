import stripe
from django.shortcuts import get_object_or_404
from djstripe.mixins import PaymentsContextMixin
from djstripe.models import Plan, Customer, APIKey
from djstripe.settings import djstripe_settings
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from web_app.models import Organization, Space


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
            context[
                'new_space_button_text'] = _('New space') if self.request.user.can_create_space is True else _(
                'Upgrade to create more spaces')
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


class SpaceMixin:
    _space = None  # Placeholder for the cached object

    def get_space(self) -> Space:
        if self._space is None:
            self._space = get_object_or_404(Space, pk=self.kwargs.get('space_uuid'),
                                            organization__in=self.request.user.organizations.all()
                                            )
        return self._space

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['space'] = self.get_space()
        data['organization'] = self.get_space().organization
        return data


class SideBarMixin:
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['sidebar'] = {'team': False, 'space': False, 'company': False, 'organization': False}
        return data


class SpaceSideBarMixin(SideBarMixin):
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['sidebar']['space'] = True
        return data
