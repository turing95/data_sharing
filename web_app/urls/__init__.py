from django.urls import path
from web_app.views import SpacesView, SpaceFormView, SpaceDetailFormViewReceiver, \
    PasswordResetView,SignupView, LoginView,SpaceDetailFormViewSender, \
    TermsOfServiceView, PrivacyPolicyView,DeleteSpaceView, custom_page_not_found, custom_server_error,toggle_sender_active,toggle_space_active

urlpatterns = [
    path('', SpacesView.as_view(), name='spaces'),
    path('accounts/signup/', SignupView.as_view(), name='account_signup'),
    path('accounts/login/', LoginView.as_view(), name='account_login'),
    path('accounts/password/reset/', PasswordResetView.as_view(), name='account_reset_password'),
    path('spaces/add/', SpaceFormView.as_view(), name='space_create'),
    path('spaces/detail/<uuid:space_uuid>/', SpaceDetailFormViewReceiver.as_view(), name='receiver_space_detail'),
    path('spaces/delete/<uuid:space_uuid>/', DeleteSpaceView.as_view(), name='space_delete'),
    path('spaces/<uuid:space_uuid>/', SpaceDetailFormViewSender.as_view(), name='sender_space_detail_public'),
    path('spaces/<uuid:space_uuid>/senders/<uuid:sender_uuid>/', SpaceDetailFormViewSender.as_view(), name='sender_space_detail_private'),
    path('spaces(<uuid:space_uuid>/toggle_active/', toggle_space_active, name='toggle_space_active'),
    path('senders(<uuid:sender_uuid>/toggle_active/',toggle_sender_active, name='toggle_sender_active'),
    path('terms_of_service/', TermsOfServiceView.as_view(), name='terms_of_service'),
    path('privacy_policy/', PrivacyPolicyView.as_view(), name='privacy_policy'),
    path("404/", custom_page_not_found),
    path("500/", custom_server_error)
]
