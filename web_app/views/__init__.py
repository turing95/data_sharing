from web_app.views.receiver.space.list import SpacesView
from web_app.views.receiver.space.create import SpaceFormView
from web_app.views.receiver.space.delete import DeleteSpaceView
from web_app.views.receiver.authentication.signup import SignupView
from web_app.views.receiver.authentication.login import LoginView,LoginCancelledView
from web_app.views.receiver.authentication.reset_password import PasswordResetView
from web_app.views.receiver.authentication.delete import AccountDeleteView
from web_app.views.receiver.authentication.connections import ConnectionsView
from web_app.views.receiver.space.detail import SpaceDetailFormView as SpaceDetailFormViewReceiver
from web_app.views.legal.terms_of_service import TermsOfServiceView
from web_app.views.legal.privacy_policy import privacy_policy
from web_app.views.legal.cookie_policy import cookie_policy
from web_app.views.public_landing import PublicLandingView
from web_app.views.receiver.settings import SettingsView
from web_app.views.beta_access_request import BetaAccessRequestFormView

from web_app.views.sender.space_detail import SpaceDetailView as SpaceDetailFormViewSender

from web_app.views.custom_http_errors import custom_page_not_found, custom_server_error

from web_app.views.api.sender import toggle_sender_active,notify_deadline,notify_invitation, sender_modal, sender_info, sender_row
from web_app.views.api.space import toggle_space_public,history_table,request_modal
from web_app.views.api.request import delete_request
from web_app.views.api.destination import search_folder, select_destination_type,get_destination_logo
from web_app.views.api.file_type import search_file_types
from web_app.views.receiver.payments.checkout import create_checkout_session
from web_app.views.receiver.payments.billing import create_billing_session

