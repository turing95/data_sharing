from web_app.views.space.list import SpacesView
from web_app.views.space.create import space_create
from web_app.views.space.detail.content import SpaceContentView
from web_app.views.space.detail.file_section.update import file_section_update
from web_app.views.space.detail.file_section.create import file_section_create
from web_app.views.space.detail.text_section.update import text_section_update
from web_app.views.space.detail.text_section.create import text_section_create
from web_app.views.space.detail.files import SpaceDocumentsView
from web_app.views.space.detail.requests import SpaceRequestsView
from web_app.views.space.detail.settings import SpaceSettingsView
from web_app.views.space.detail.history import HistoryListView
from web_app.views.space.update import space_update
from web_app.views.space.sender.detail import SpaceDetailView as SpaceDetailFormViewSender
from web_app.views.space.sender.request.list import RequestListView as RequestListViewSender
from web_app.views.request.create import request_create
from web_app.views.request.detail.edit import RequestEditView, request_title_update, request_instructions_update
from web_app.views.request.detail.content import RequestDetailView
from web_app.views.request.update import request_update_order, input_requests
from web_app.views.space.detail.section.update import space_section_update_order, sections
from web_app.views.space.detail.section.delete import section_delete
from web_app.views.request.sender import RequestDetailView as SenderRequestDetailView
from web_app.views.upload_request.create import upload_request_create
from web_app.views.upload_request.update import upload_request_update
from web_app.views.input_request.update import input_request_update_active, input_request_update_complete
from web_app.views.input_request.detail import input_request_detail_show
from web_app.views.input_request.delete import input_request_delete
from web_app.views.output.update import accept as output_accept, reject as output_reject
from web_app.views.output.detail import output_detail, output_reject_modal
from web_app.views.upload_request.detail import upload_request_detail_show
from web_app.views.text_request.update import text_request_update
from web_app.views.text_request.create import text_request_create
from web_app.views.event.upload_history import history_table
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

from web_app.views.sender.detail import (toggle_sender_active, notify_deadline, notify_invitation,
                                         sender_row, bulk_notify_invitation, bulk_notify_deadline,
                                         sender_upload_notification, sender_notify, sender_notify_modal)
from web_app.views.sender.create import sender_create_row, sender_contact_update
from web_app.views.organization.create import create_organization, create_organization_modal
from web_app.views.organization.settings import OrganizationSettingsView
from web_app.views.organization.delete import OrganizationDeleteView
from web_app.views.organization.update import organization_update
from web_app.views.destination import search_folder, select_destination_type, get_destination_logo
from web_app.views.profile import profile
from web_app.views.file import request_changes, accept_all, accept_single
from web_app.views.settings import sender_notifications_settings_update, account_notifications
from web_app.views.payments.checkout import create_checkout_session
from web_app.views.payments.billing import create_billing_session
from web_app.views.djstripe_webhooks.payment import custom_webhook
from web_app.views.company.list import CompanyListView, search_companies
from web_app.views.company.create import CompanyCreateView
from web_app.views.company.detail.home import CompanyDetailView
from web_app.views.company.delete import CompanyDeleteView
from web_app.views.company.detail.spaces import CompanySpacesListView
from web_app.views.company.detail.contacts import CompanyContactsListView
from web_app.views.company.detail.files import CompanyFilesListView
from web_app.views.company.update import company_update_name, company_update
from web_app.views.fields.update import text_field_update, text_field_update_modal, \
    text_field_update_value, field_group_update, field_group_update_modal, \
    field_group_add_template, file_field_update, file_field_update_modal
from web_app.views.fields.create import text_field_create_modal,file_field_create_modal,file_field_create, text_field_create, \
    text_field_duplicate, field_group_create_modal, field_group_create, \
    field_group_to_template, field_group_duplicate, file_field_duplicate
from web_app.views.fields.delete import text_field_delete, field_group_delete, file_field_delete
from web_app.views.fields.detail import text_field_detail, file_field_detail
from web_app.views.fields.list import group_elements, group_elements_update_order
from web_app.views.field_group_templates.list import FieldGroupTemplatesListView, search_templates
from web_app.views.field_group_templates.detail import FieldGroupTemplateDetailView
from web_app.views.field_group_templates.delete import FieldGroupTemplateDeleteView
from web_app.views.language import custom_set_language, language_modal
from web_app.views.contact.create import ContactCreateView, contact_create_modal
from web_app.views.contact.delete import DeleteContactView
from web_app.views.contact.detail import ContactDetailView
from web_app.views.contact.list import ContactListView, search_contacts
from web_app.views.grant.create import grant_create
from web_app.views.grant.detail import GrantDetailView
from web_app.views.grant.list import GrantListView
from web_app.views.grant.delete import GrantDeleteView
from web_app.views.grant.update import grant_update_name, grant_update, GrantEditView
