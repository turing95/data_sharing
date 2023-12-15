from web_app.views.receiver.space.list import SpacesView
from web_app.views.receiver.space.create import SpaceFormView
from web_app.views.receiver.space.delete import DeleteSpaceView
from web_app.views.receiver.authentication.signup import SignupView
from web_app.views.receiver.authentication.login import LoginView
from web_app.views.receiver.authentication.reset_password import PasswordResetView
from web_app.views.receiver.space.detail import SpaceDetailFormView as SpaceDetailFormViewReceiver
from web_app.views.receiver.terms_of_service import TermsOfServiceView
from web_app.views.receiver.privacy_policy import PrivacyPolicyView
from web_app.views.sender.space_detail import SpaceDetailView as SpaceDetailFormViewSender
from web_app.views.api.sender import toggle_sender_active
from web_app.views.custom_http_errors import custom_page_not_found, custom_server_error

