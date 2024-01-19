from django.urls import path
from web_app.views import SpacesView, SpaceFormView, SpaceDetailFormViewReceiver, \
    PasswordResetView, SignupView, LoginView, SpaceDetailFormViewSender, \
    TermsOfServiceView, PrivacyPolicyView, DeleteSpaceView, SettingsView, PublicLandingView, \
    custom_page_not_found, custom_server_error, toggle_sender_active, delete_request, \
    toggle_space_public, history_table, \
    request_modal, create_checkout_session, search_file_types,notify_deadline,notify_invitation,create_billing_session

urlpatterns = [
    # Generic views
    path('terms-of-service/', TermsOfServiceView.as_view(), name='generic_terms_of_service'),
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='generic_privacy_policy'),
    path('', PublicLandingView.as_view(), name='generic_home'),
    # Receiver views
    path('spaces/', SpacesView.as_view(), name='spaces'),
    path('accounts/login/', LoginView.as_view(), name='account_login'),
    path('accounts/settings/', SettingsView.as_view(), name='account_settings'),
    path('spaces/add/', SpaceFormView.as_view(), name='space_create'),
    path('spaces/detail/<uuid:space_uuid>/', SpaceDetailFormViewReceiver.as_view(), name='receiver_space_detail'),
    path('spaces/delete/<uuid:space_uuid>/', DeleteSpaceView.as_view(), name='space_delete'),
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
    path('spaces/<uuid:space_uuid>/toggle-public/', toggle_space_public, name='toggle_space_public'),
    path('spaces/<uuid:space_uuid>/history-table/', history_table, name='history_table'),
    path('request/<uuid:request_uuid>/modal/', request_modal, name='request_modal'),
    path('requests/<uuid:request_uuid>/delete/', delete_request, name='request_delete'),
    path('senders/<uuid:sender_uuid>/toggle-active/', toggle_sender_active, name='toggle_sender_active'),
    path('senders/<uuid:sender_uuid>/notify_deadline/', notify_deadline, name='notify_deadline'),
    path('senders/<uuid:sender_uuid>/notify_invitation/', notify_invitation, name='notify_invitation'),
]
