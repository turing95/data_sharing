from web_app.views.receiver.space.list import SpacesView
from web_app.views.receiver.space.create import SpaceCreateView
from web_app.views.receiver.request.create import RequestCreateView
from web_app.views.receiver.request.detail import RequestDetailView
from web_app.views.receiver.event.upload_history import UploadHistoryListView
from web_app.views.receiver.sender.list import SenderListView
from web_app.views.receiver.space.delete import DeleteSpaceView
from web_app.views.receiver.space.duplicate import duplicate
from web_app.views.receiver.authentication.signup import SignupView
from web_app.views.receiver.organization.team import TeamView, team_invitation, team_invitation_redemption, \
    revoke_invitation, remove_team_member
from web_app.views.receiver.authentication.login import LoginView, LoginCancelledView
from web_app.views.receiver.authentication.reset_password import PasswordResetView, PasswordResetDoneView, \
    PasswordResetFromKeyView, PasswordResetFromKeyDoneView
from web_app.views.receiver.authentication.delete import AccountDeleteView
from web_app.views.receiver.authentication.connections import ConnectionsView
from web_app.views.api.profile import profile
from web_app.views.receiver.space.detail import SpaceSettingsView, SpaceDetailView
from web_app.views.legal.terms_of_service import TermsOfServiceView
from web_app.views.legal.privacy_policy import privacy_policy
from web_app.views.legal.cookie_policy import cookie_policy
from web_app.views.public_landing import PublicLandingView
from web_app.views.receiver.settings import SettingsView
from web_app.views.beta_access_request import BetaAccessRequestFormView

from web_app.views.sender.space_detail import SpaceDetailView as SpaceDetailFormViewSender

from web_app.views.custom_http_errors import custom_page_not_found, custom_server_error

from web_app.views.api.sender import (toggle_sender_active, notify_deadline, notify_invitation, sender_modal,
                                      sender_info,
                                      sender_row, all_senders_modal, bulk_notify_invitation, bulk_notify_deadline,
                                      sender_upload_notification)
from web_app.views.api.space import toggle_space_public, history_table, request_modal
from web_app.views.api.request import delete_request
from web_app.views.api.organization import create_organization, create_organization_modal
from web_app.views.api.destination import search_folder, select_destination_type, get_destination_logo
from web_app.views.api.file_type import search_file_types
from web_app.views.api.profile import profile
from web_app.views.api.file import request_changes, accept_all, accept_single
from web_app.views.api.settings import sender_notifications_settings, account_notifications
from web_app.views.receiver.payments.checkout import create_checkout_session
from web_app.views.receiver.payments.billing import create_billing_session
from web_app.views.djstripe_webhooks.payment import custom_webhook
from web_app.views.receiver.organization.company import CompanyListView, CompanyCreateView, CompanyDetailView, CompanySpacesListView, search_companies
from web_app.views.language import custom_set_language
from web_app.views.receiver.organization.contact import ContactListView, search_contacts, contact_create_modal, contact_create, ContactCreateView
