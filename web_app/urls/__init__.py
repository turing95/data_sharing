from django.urls import path
from web_app.views import SpacesView, SpaceFormView, SpaceDetailFormViewReceiver, \
    PasswordResetView, SignupView, LoginView, SpaceDetailFormViewSender, \
    TermsOfServiceView, PrivacyPolicyView, DeleteSpaceView, SettingsView, PublicLandingView, \
    custom_page_not_found, custom_server_error, toggle_sender_active, toggle_space_active,delete_request,toggle_space_public,history_table, \
    request_modal

urlpatterns = [
    path('spaces/', SpacesView.as_view(), name='spaces'),
    path('accounts/signup/', SignupView.as_view(), name='account_signup'),
    path('accounts/login/', LoginView.as_view(), name='account_login'),
    path('accounts/password/reset/', PasswordResetView.as_view(), name='account_reset_password'),
    path('accounts/settings/', SettingsView.as_view(), name='account_settings'),
    path('spaces/add/', SpaceFormView.as_view(), name='space_create'),
    path('spaces/detail/<uuid:space_uuid>/', SpaceDetailFormViewReceiver.as_view(), name='receiver_space_detail'),
    path('spaces/delete/<uuid:space_uuid>/', DeleteSpaceView.as_view(), name='space_delete'),
    path('upload/<uuid:space_uuid>/', SpaceDetailFormViewSender.as_view(), name='sender_space_detail_public'),
    path('upload/<uuid:space_uuid>/senders/<uuid:sender_uuid>/', SpaceDetailFormViewSender.as_view(),
         name='sender_space_detail_private'),

    path('spaces/<uuid:space_uuid>/toggle_active/', toggle_space_active, name='toggle_space_active'),
    path('spaces/<uuid:space_uuid>/toggle_public/', toggle_space_public, name='toggle_space_public'),
    path('spaces/<uuid:space_uuid>/history_table/', history_table, name='history_table'),

    path('request/<uuid:request_uuid>/modal/', request_modal, name='request_modal'),

    path('requests/<uuid:request_uuid>/delete/', delete_request, name='request_delete'),

    path('senders/<uuid:sender_uuid>/toggle_active/', toggle_sender_active, name='toggle_sender_active'),
    path('terms_of_service/', TermsOfServiceView.as_view(), name='terms_of_service'),
    path('privacy_policy/', PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('', PublicLandingView.as_view(), name='home'),
    path("404/", custom_page_not_found),
    path("500/", custom_server_error)
]
