import stripe
from django.shortcuts import get_object_or_404
from djstripe.mixins import PaymentsContextMixin
from djstripe.models import Plan, Customer, APIKey
from djstripe.settings import djstripe_settings
from web_app.utils.svg_icon_paths import svg_icons_path as paths
from django.utils.translation import gettext_lazy as _

from web_app.models import Organization, Space, Request, Company, Sender, Grant


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


class GrantMixin:
    _grant = None  # Placeholder for the cached object

    def get_grant(self):
        if not self._grant:
            self._grant = Grant.objects.get(pk=self.kwargs.get('grant_uuid'))
        return self._grant

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grant'] = self.get_grant()
        context['organization'] = self.get_grant().organization
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
        data['sidebar'] = {'team': False, 'space': False, 'company': False, 'organization': False, 'grant': False}
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


class GrantSideBarMixin(SideBarMixin):
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['sidebar']['grant'] = True
        return data


class CompanyTabMixin:
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['company_tab'] = {
            'detail': {
                'active': False,
                'alternative_text': _('Detail'),
                'url_name': 'company_detail',
                'svg_path': paths['detail']
            },
            # 'contacts': {
            #     'active': False,
            #     'alternative_text': _('Contacts'),
            #     'url_name': 'company_contacts',
            #     'svg_path': paths['contacts']
            # },
            'spaces': {
                'active': False,
                'alternative_text': _('Spaces'),
                'url_name': 'company_spaces',
                'svg_path': paths['spaces']
            },
            # 'requests': {
            #     'active': False,
            #     'alternative_text': _('Requests'),
            #     'url_name': 'company_detail',
            #     'svg_path': paths['requests']
            # },

            'documents': {
                'active': False,
                'alternative_text': _('Documents'),
                'url_name': 'company_files',
                'svg_path': paths['documents']
            },

        }
        return data


class RequestTabMixin:

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['request_tab'] = {
            'content_inbox': {
                'active': False,
                'alternative_text': _('Content Inbox'),
                'url_name': 'request_detail',
                'svg_path': paths['inbox']
            },
            'edit': {
                'active': False,
                'alternative_text': _('Edit'),
                'url_name': 'request_detail',
                'svg_path': paths['edit']
            },
            'history': {
                'active': False,
                'alternative_text': _('History'),
                'url_name': 'request_detail',
                'svg_path': paths['history']
            },

        }
        return data


class SpaceTabMixin:
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['space_tab'] = {
            'content': {
                'active': False,
                'alternative_text': _('Content'),
                'url_name': 'space_content',
                'svg_path': paths['content']
            },
            'requests': {
                'active': False,
                'alternative_text': _('Requests'),
                'url_name': 'receiver_space_detail',
                'svg_path': paths['requests']
            },
            'share': {
                'active': False,
                'alternative_text': _('Share'),
                'url_name': 'senders',
                'svg_path': paths['share']
            },
            'history': {
                'active': False,
                'alternative_text': _('History'),
                'url_name': 'space_history',
                'svg_path': paths['history']
            },
            'documents': {
                'active': False,
                'alternative_text': _('Documents'),
                'url_name': "space_documents",
                'svg_path': paths['documents']
            },
            'settings': {
                'active': False,
                'alternative_text': _('Settings'),
                'url_name': 'space_settings',
                'svg_path': paths['settings']
            },

        }
        return data


class SpaceSenderMixin:
    _sender = None
    _space = None

    def get_sender(self):
        if not self._sender:
            self._sender = get_object_or_404(Sender, pk=self.kwargs.get('sender_uuid'), is_active=True)
        return self._sender

    def get_space(self):
        if not self._space:
            space_id = self.kwargs.get('space_uuid')
            sender = self.get_sender()

            filter_criteria = {
                'pk': space_id,
                'is_deleted': False,
                'senders__uuid': sender.pk
            }
            self._space = get_object_or_404(Space, **filter_criteria)
        return self._space

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['sender'] = self.get_sender()
        data['space'] = self.get_space()
        return data


class SenderTabMixin:
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['sender_tab'] = {
            'detail': {
                'active': False,
                'alternative_text': _('Content'),
                'url_name': 'sender_space_detail',
                'svg_path': paths['content']
            },
            'requests': {
                'active': False,
                'alternative_text': _('Requests'),
                'url_name': 'sender_space_requests',
                'svg_path': paths['requests']
            }

        }
        return data
