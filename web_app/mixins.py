import stripe
from django.shortcuts import get_object_or_404
from djstripe.mixins import PaymentsContextMixin
from djstripe.models import Plan, Customer, APIKey
from djstripe.settings import djstripe_settings
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from web_app.models import Organization, Space, UploadRequest, Request, Company


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

class CompanyMixin:
    _company = None  # Placeholder for the cached object
    
    def get_company(self):
        if not self._company:
            self._company = Company.objects.get(pk=self.kwargs.get('company_uuid'))
        return self._company

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['organization'] = self.get_company().organization
        context['company'] = self.get_company()
        return context

class RequestMixin:
    _request = None  # Placeholder for the cached object

    def get_request(self) -> Request:
        if self._request is None:
            self._request = get_object_or_404(Request, pk=self.kwargs.get('request_uuid'))
        return self._request

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['kezyy_request'] = self.get_request()
        data['space'] = self.get_request().space
        data['organization'] = self.get_request().space.organization
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


class ContactSideBarMixin(SideBarMixin):
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['sidebar']['contact'] = True
        return data


class CompanySideBarMixin(SideBarMixin):
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['sidebar']['company'] = True
        return data


class CompanyTabMixin:
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['company_tab'] = {
            'detail': {
                'active': False,
                'alternative_text': _('Detail'),
                'url_name': 'company_detail',
                'svg_path': "M8.25 6.75h12M8.25 12h12m-12 5.25h12M3.75 6.75h.007v.008H3.75V6.75Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0ZM3.75 12h.007v.008H3.75V12Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm-.375 5.25h.007v.008H3.75v-.008Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z",  # SVG path for the icon
            },
            # 'contacts': {
            #     'active': False,
            #     'alternative_text': _('Contacts'),
            #     'url_name': 'company_contacts',
            #     'svg_path': "M15 9h3.75M15 12h3.75M15 15h3.75M4.5 19.5h15a2.25 2.25 0 0 0 2.25-2.25V6.75A2.25 2.25 0 0 0 19.5 4.5h-15a2.25 2.25 0 0 0-2.25 2.25v10.5A2.25 2.25 0 0 0 4.5 19.5Zm6-10.125a1.875 1.875 0 1 1-3.75 0 1.875 1.875 0 0 1 3.75 0Zm1.294 6.336a6.721 6.721 0 0 1-3.17.789 6.721 6.721 0 0 1-3.168-.789 3.376 3.376 0 0 1 6.338 0Z",  # SVG path for the icon
            # },
            'spaces': {
                'active': False,
                'alternative_text': _('Spaces'),
                'url_name': 'company_spaces',
                'svg_path': "M3.75 6A2.25 2.25 0 0 1 6 3.75h2.25A2.25 2.25 0 0 1 10.5 6v2.25a2.25 2.25 0 0 1-2.25 2.25H6a2.25 2.25 0 0 1-2.25-2.25V6ZM3.75 15.75A2.25 2.25 0 0 1 6 13.5h2.25a2.25 2.25 0 0 1 2.25 2.25V18a2.25 2.25 0 0 1-2.25 2.25H6A2.25 2.25 0 0 1 3.75 18v-2.25ZM13.5 6a2.25 2.25 0 0 1 2.25-2.25H18A2.25 2.25 0 0 1 20.25 6v2.25A2.25 2.25 0 0 1 18 10.5h-2.25a2.25 2.25 0 0 1-2.25-2.25V6ZM13.5 15.75a2.25 2.25 0 0 1 2.25-2.25H18a2.25 2.25 0 0 1 2.25 2.25V18A2.25 2.25 0 0 1 18 20.25h-2.25A2.25 2.25 0 0 1 13.5 18v-2.25Z",  # SVG path for the icon
            },
            # 'requests': {
            #     'active': False,
            #     'alternative_text': _('Requests'),
            #     'url_name': 'company_detail',
            #     'svg_path': "M8.25 6.75h12M8.25 12h12m-12 5.25h12M3.75 6.75h.007v.008H3.75V6.75Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0ZM3.75 12h.007v.008H3.75V12Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm-.375 5.25h.007v.008H3.75v-.008Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z",  # SVG path for the icon
            # },
            'documents': {
                'active': False,
                'alternative_text': _('Documents'),
                'url_name': 'company_files',
                'svg_path': "M8.25 6.75h12M8.25 12h12m-12 5.25h12M3.75 6.75h.007v.008H3.75V6.75Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0ZM3.75 12h.007v.008H3.75V12Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm-.375 5.25h.007v.008H3.75v-.008Zm.375 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z",  # SVG path for the icon
            },
        }
        return data