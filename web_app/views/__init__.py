from web_app.views.space.list import SpacesView
from web_app.views.space.create import SpaceCreateView, space_create
from web_app.views.space.detail import SpaceSettingsView, SpaceDetailView, space_edit
from web_app.views.space.sender.detail import SpaceDetailView as SpaceDetailFormViewSender
from web_app.views.request.create import RequestCreateView, request_create
from web_app.views.request.detail import RequestDetailView, request_modal
from web_app.views.request.sender import RequestDetailView as SenderRequestDetailView
from web_app.views.upload_request.create import upload_request_create
from web_app.views.upload_request.update import upload_request_update
from web_app.views.text_request.update import text_request_update
from web_app.views.text_request.create import text_request_create
from web_app.views.event.upload_history import UploadHistoryListView, history_table
from web_app.views.sender.list import SenderListView
from web_app.views.space.delete import DeleteSpaceView
from web_app.views.space.duplicate import duplicate
from web_app.views.authentication.signup import SignupView
from web_app.views.organization.team import TeamView, team_invitation, team_invitation_redemption, \
    revoke_invitation, remove_team_member
from web_app.views.authentication.login import LoginView, LoginCancelledView
from web_app.views.authentication.reset_password import PasswordResetView, PasswordResetDoneView, \
    PasswordResetFromKeyView, PasswordResetFromKeyDoneView
from web_app.views.authentication.delete import AccountDeleteView
from web_app.views.authentication.connections import ConnectionsView
from web_app.views.profile import profile
from web_app.views.legal.terms_of_service import TermsOfServiceView
from web_app.views.legal.privacy_policy import privacy_policy
from web_app.views.legal.cookie_policy import cookie_policy
from web_app.views.public_landing import PublicLandingView
from web_app.views.settings import SettingsView
from web_app.views.beta_access_request import BetaAccessRequestFormView
from web_app.views.custom_http_errors import custom_page_not_found, custom_server_error

from web_app.views.sender.detail import (toggle_sender_active, notify_deadline, notify_invitation, sender_modal,
                                      sender_info,
                                      sender_row, all_senders_modal, bulk_notify_invitation, bulk_notify_deadline,
                                      sender_upload_notification)
from web_app.views.request.delete import delete_request
from web_app.views.organization.create import create_organization, create_organization_modal
from web_app.views.destination import search_folder, select_destination_type, get_destination_logo
from web_app.views.profile import profile
from web_app.views.file import request_changes, accept_all, accept_single
from web_app.views.settings import sender_notifications_settings, account_notifications
from web_app.views.payments.checkout import create_checkout_session
from web_app.views.payments.billing import create_billing_session
from web_app.views.djstripe_webhooks.payment import custom_webhook
from web_app.views.organization.company import CompanyListView, CompanyCreateView, CompanyDetailView, CompanySpacesListView, search_companies
from web_app.views.language import custom_set_language
from web_app.views.organization.contact import ContactListView, search_contacts, contact_create_modal, contact_create, ContactCreateView
