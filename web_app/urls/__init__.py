from django.urls import path
from web_app.views import SpacesView, SpaceFormView, SpaceDetailFormViewReceiver, \
    PasswordResetView,SignupView, LoginView,SpaceDetailFormViewSender, \
    TermsOfServiceView, PrivacyPolicyView,delete_space

urlpatterns = [
    path('', SpacesView.as_view(), name='spaces'),
    path('accounts/signup/', SignupView.as_view(), name='account_signup'),
    path('accounts/login/', LoginView.as_view(), name='account_login'),
    path('accounts/password/reset/', PasswordResetView.as_view(), name='account_reset_password'),
    path('spaces/add/', SpaceFormView.as_view(), name='space_create'),
    path('spaces/detail/<uuid:space_uuid>/', SpaceDetailFormViewReceiver.as_view(), name='receiver_space_detail'),
    path('spaces/delete/<uuid:space_uuid>/', delete_space, name='space_delete'),
    path('spaces/<uuid:space_uuid>/', SpaceDetailFormViewSender.as_view(), name='sender_space_detail_public'),
    path('spaces/<uuid:space_uuid>/senders/<uuid:sender_uuid>/', SpaceDetailFormViewSender.as_view(), name='sender_space_detail_private'),
    path('terms_of_service/', TermsOfServiceView.as_view(), name='terms_of_service'),
    path('privacy_policy/', PrivacyPolicyView.as_view(), name='privacy_policy'),
]
