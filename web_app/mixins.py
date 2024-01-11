from djstripe.mixins import PaymentsContextMixin
from djstripe.models import Plan, Customer
from djstripe.settings import djstripe_settings
from django.conf import settings


class SubscriptionMixin(PaymentsContextMixin):
    """Adds customer subscription context to a view."""

    def get_context_data(self, *args, **kwargs):
        """Inject is_plans_plural and customer into context_data."""
        context = super().get_context_data(**kwargs)
        context["is_plans_plural"] = Plan.objects.count() > 1
        if self.request.user.is_authenticated:
            context["customer"], _created = Customer.get_or_create(
                subscriber=djstripe_settings.subscriber_request_callback(self.request)
            )
            context["subscription"] = context["customer"].subscription
            
            if context["subscription"] is None:
                context['user_maxed_spaces'] = self.request.user.spaces.count() >= settings.MAX_FREE_SPACES                
        return context
