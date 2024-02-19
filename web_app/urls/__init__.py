from django.urls import path, re_path
from web_app.views import SpacesView, SpaceFormView, SpaceDetailFormViewReceiver, \
    profile, LoginView, LoginCancelledView, SpaceDetailFormViewSender, \
    TermsOfServiceView, privacy_policy, cookie_policy, DeleteSpaceView, SettingsView, PublicLandingView, \
    BetaAccessRequestFormView, sender_notifications_settings, \
    custom_page_not_found, custom_server_error, toggle_sender_active, delete_request, \
    toggle_space_public, history_table, \
    request_modal, create_checkout_session, search_file_types, notify_deadline, notify_invitation, \
    create_billing_session, AccountDeleteView, sender_modal, search_folder, ConnectionsView, \
    sender_info, sender_row, select_destination_type, get_destination_logo, all_senders_modal, bulk_notify_invitation, \
    bulk_notify_deadline, duplicate, search_contacts, create_contact_modal, create_contact, request_changes, accept_all, \
    accept_single, SignupView, PasswordResetView, PasswordResetDoneView, PasswordResetFromKeyView, \
    PasswordResetFromKeyDoneView, sender_upload_notification, account_notifications

from web_app.views.language import custom_set_language
urlpatterns = [
    # Generic views
    path('accounts/set-language/', custom_set_language, name='set_user_language'),
    path('terms-of-service/', TermsOfServiceView.as_view(), name='generic_terms_of_service'),
    path('privacy-policy/', privacy_policy, name='generic_privacy_policy'),
    path('cookie-policy/', cookie_policy, name='generic_cookie_policy'),
    path('beta/', BetaAccessRequestFormView.as_view(), name='generic_beta_access'),
    path('', PublicLandingView.as_view(), name='generic_home'),
    # Receiver views
    path('spaces/', SpacesView.as_view(), name='spaces'),
    path('accounts/signup/', SignupView.as_view(), name='account_signup'),
    path('accounts/login/', LoginView.as_view(), name='account_login'),
    path('accounts/social/signup/', LoginView.as_view(), name='account_login'),
    path('accounts/password/reset/', PasswordResetView.as_view(), name='account_reset_password'),
    path(
        "accounts/password/reset/key/done/",
        PasswordResetFromKeyDoneView.as_view(),
        name="account_reset_password_from_key_done",
    ),
    path('accounts/password/reset/done/', PasswordResetDoneView.as_view(), name='account_reset_password_done'),
    re_path(
        r"^accounts/password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$", PasswordResetFromKeyView.as_view(), name='account_reset_password_from_key'),
    path('accounts/profile/', profile, name='account_profile'),
    path('accounts/settings/', SettingsView.as_view(), name='account_settings'),
    path('accounts/sender-notifications-settings/', sender_notifications_settings, name='account_sender_notifications'),
    path('accounts/notifications-settings/', account_notifications, name='account_notifications'),
    path('accounts/delete/', AccountDeleteView.as_view(), name='account_delete'),
    path('accounts/social/connections/', ConnectionsView.as_view(), name='socialaccount_connections'),
    path('accounts/social/login/cancelled/', LoginCancelledView.as_view(), name='socialaccount_login_cancelled'),
    path('spaces/add/', SpaceFormView.as_view(), name='space_create'),
    path('spaces/detail/<uuid:space_uuid>/', SpaceDetailFormViewReceiver.as_view(), name='receiver_space_detail'),
    path('spaces/delete/<uuid:space_uuid>/', DeleteSpaceView.as_view(), name='space_delete'),
    path('spaces/duplicate/<uuid:space_uuid>/', duplicate, name='space_duplicate'),
    path('stripe/create-checkout-session/', create_checkout_session, name='create_checkout_session'),
    path('stripe/create-billing-session/', create_billing_session, name='create_billing_session'),
    # Sender views
    path('spaces/<uuid:space_uuid>/', SpaceDetailFormViewSender.as_view(), name='sender_space_detail_public'),
    path('spaces/<uuid:space_uuid>/senders/<uuid:sender_uuid>/', SpaceDetailFormViewSender.as_view(),
         name='sender_space_detail_private'),
    # Error views
    path("404/", custom_page_not_found),
    path("500/", custom_server_error),
    # Ajax views
    path('file-types/search/', search_file_types, name='search_file_types'),
    path('files/<uuid:file_uuid>/accept/', accept_single, name='accept_single'),
    path('destinations/search-folder/', search_folder, name='search_folders'),
    path('destinations/select-type/', select_destination_type, name='select_destination_type'),
    path('destinations/get-logo/', get_destination_logo, name='get_destination_logo'),
    path('spaces/<uuid:space_uuid>/toggle-public/', toggle_space_public, name='toggle_space_public'),
    path('spaces/<uuid:space_uuid>/history-table/', history_table, name='history_table'),
    path('spaces/<uuid:space_uuid>/all-senders-modal/', all_senders_modal, name='all_senders_modal'),
    path('spaces/<uuid:space_uuid>/invite-all-senders/', bulk_notify_invitation, name='bulk_notify_invitation'),
    path('spaces/<uuid:space_uuid>/notify-all-senders/', bulk_notify_deadline, name='bulk_notify_deadline'),
    path('requests/<uuid:request_uuid>/modal/', request_modal, name='request_modal'),
    path('requests/<uuid:request_uuid>/files/changes/', request_changes, name='request_changes'),
    path('requests/<uuid:request_uuid>/files/accept/', accept_all, name='accept_all'),
    path('requests/<uuid:request_uuid>/delete/', delete_request, name='request_delete'),
    path('spaces/<uuid:space_uuid>/senders-history-table/', history_table, name='sender_history_table'),
    path('senders/<uuid:sender_uuid>/modal/', sender_modal, name='sender_modal'),
    path('senders/<uuid:sender_uuid>/sender-info/', sender_info, name='sender_info'),
    path('senders/<uuid:sender_uuid>/sender-row/', sender_row, name='sender_row'),
    path('senders/<uuid:sender_uuid>/toggle-active/', toggle_sender_active, name='toggle_sender_active'),
    path('senders/<uuid:sender_uuid>/notify_deadline/', notify_deadline, name='notify_deadline'),
    path('senders/<uuid:sender_uuid>/notify_invitation/', notify_invitation, name='notify_invitation'),
    path('senders/sender-upload-notification/', sender_upload_notification, name='sender_upload_notification'),
    path('contacts/search/', search_contacts, name='search_contacts'),
    path('contacts/create/modal/', create_contact_modal, name='create_contact_modal'),
    path('contacts/create/', create_contact, name='create_contact'),
]
