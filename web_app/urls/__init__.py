from django.urls import path, re_path
from web_app import views

urlpatterns = [
    # Generic views
    path('accounts/set-language/', views.custom_set_language, name='set_user_language'),
    path('terms-of-service/', views.TermsOfServiceView.as_view(), name='generic_terms_of_service'),
    path('privacy-policy/', views.privacy_policy, name='generic_privacy_policy'),
    path('cookie-policy/', views.cookie_policy, name='generic_cookie_policy'),
    path('beta/', views.BetaAccessRequestFormView.as_view(), name='generic_beta_access'),
    path('', views.PublicLandingView.as_view(), name='generic_home'),
    # Receiver views
    path('accounts/signup/', views.SignupView.as_view(), name='account_signup'),
    path('accounts/login/', views.LoginView.as_view(), name='account_login'),
    path('accounts/social/signup/', views.LoginView.as_view(), name='account_login'),
    path('accounts/password/reset/', views.PasswordResetView.as_view(), name='account_reset_password'),
    path(
        "accounts/password/reset/key/done/",
        views.PasswordResetFromKeyDoneView.as_view(),
        name="account_reset_password_from_key_done",
    ),
    path('accounts/password/reset/done/', views.PasswordResetDoneView.as_view(), name='account_reset_password_done'),
    re_path(
        r"^accounts/password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        views.PasswordResetFromKeyView.as_view(), name='account_reset_password_from_key'),
    path('accounts/profile/', views.profile, name='account_profile'),
    path('accounts/settings/', views.SettingsView.as_view(), name='account_settings'),
    path('accounts/sender-notifications-settings/', views.sender_notifications_settings,
         name='account_sender_notifications'),
    path('accounts/notifications-settings/', views.account_notifications, name='account_notifications'),
    path('accounts/delete/', views.AccountDeleteView.as_view(), name='account_delete'),
    path('accounts/social/connections/', views.ConnectionsView.as_view(), name='socialaccount_connections'),
    path('accounts/social/login/cancelled/', views.LoginCancelledView.as_view(), name='socialaccount_login_cancelled'),
    path('organizations/<uuid:organization_uuid>/spaces/', views.SpacesView.as_view(), name='spaces'),
    path('spaces/', views.SpacesView.as_view(), name='spaces'),
    path('organizations/<uuid:organization_uuid>/spaces/create/', views.space_create, name='space_create'),
    path('organizations/<uuid:organization_uuid>/companies/create/', views.CompanyCreateView.as_view(),
         name='company_create'),
    path('organizations/<uuid:organization_uuid>/companies/search/', views.search_companies, name='search_companies'),
    path('organizations/<uuid:organization_uuid>/companies/', views.CompanyListView.as_view(), name='companies'),
    path('companies/<uuid:company_uuid>/detail/', views.CompanyDetailView.as_view(), name='company_detail'),
    path('companies/<uuid:company_uuid>/spaces/', views.CompanySpacesListView.as_view(), name='company_spaces'),
    path('companies/<uuid:company_uuid>/contacts/', views.CompanyContactsListView.as_view(), name='company_contacts'),
    path('companies/<uuid:company_uuid>/files/', views.CompanyFilesListView.as_view(), name='company_files'),
    path('organizations/<uuid:organization_uuid>/contacts/', views.ContactListView.as_view(), name='contacts'),
    path('spaces/<uuid:space_uuid>/detail/', views.SpaceDetailView.as_view(), name='receiver_space_detail'),
    path('spaces/<uuid:space_uuid>/settings/', views.SpaceSettingsView.as_view(), name='space_settings'),
    path('spaces/<uuid:space_uuid>/history/', views.HistoryListView.as_view(), name='space_history'),
    path('spaces/<uuid:space_uuid>/senders/', views.SenderListView.as_view(), name='senders'),
    path('spaces/<uuid:space_uuid>/requests/create/', views.request_create, name='request_create'),
    path('requests/<uuid:request_uuid>/detail/', views.RequestDetailView.as_view(), name='request_detail'),
    path('requests/<uuid:request_uuid>/update/', views.request_update_order, name='request_update_order'),
    path('requests/<uuid:request_uuid>/upload-requests/create/', views.upload_request_create,
         name='upload_request_create'),
    path('upload-requests/<uuid:upload_request_uuid>/update/', views.upload_request_update,
         name='upload_request_update'),
    path('upload-requests/<uuid:upload_request_uuid>/detail-show/', views.upload_request_detail_show,
         name='upload_request_detail_show'),
    path('requests/<uuid:request_uuid>/text-requests/create/', views.text_request_create, name='text_request_create'),
    path('text-requests/<uuid:text_request_uuid>/update/', views.text_request_update,
         name='text_request_update'),
    path('organizations/<uuid:organization_uuid>/team/', views.TeamView.as_view(), name='team'),
    path('organizations/<uuid:organization_uuid>/team-invitation/', views.team_invitation, name='team_invitation'),
    path('team-invitation-redemption/', views.team_invitation_redemption, name='team_invitation_redemption'),
    path('<uuid:invitation_uuid>/revoke-invitation/', views.revoke_invitation, name='revoke_invitation'),
    path('<uuid:user_org_uuid>/delete/', views.remove_team_member, name='remove_team_member'),
    path('spaces/delete/<uuid:space_uuid>/', views.DeleteSpaceView.as_view(), name='space_delete'),
    path('spaces/duplicate/<uuid:space_uuid>/', views.duplicate, name='space_duplicate'),
    path('stripe/create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('stripe/create-billing-session/', views.create_billing_session, name='create_billing_session'),
    # Sender views
    path('spaces/<uuid:space_uuid>/', views.SpaceDetailFormViewSender.as_view(), name='sender_space_detail_public'),
    path('senders/<uuid:sender_uuid>/spaces/<uuid:space_uuid>/', views.SpaceDetailFormViewSender.as_view(),
         name='sender_space_detail'),
    path('senders/<uuid:sender_uuid>/request/<uuid:request_uuid>/', views.SenderRequestDetailView.as_view(),
         name='sender_request_detail'),
    # Error views
    path("404/", views.custom_page_not_found),
    path("500/", views.custom_server_error),
    # Ajax views
    path('files/<uuid:file_uuid>/accept/', views.accept_single, name='accept_single'),
    path('upload-requests/<uuid:upload_request_uuid>/destinations/search-folder/', views.search_folder,
         name='search_folders'),
    path('upload-requests/<uuid:upload_request_uuid>/destinations/select-type/', views.select_destination_type,
         name='select_destination_type'),
    path('upload-requests/<uuid:upload_request_uuid>/destinations/get-logo/', views.get_destination_logo,
         name='get_destination_logo'),
    path('spaces/<uuid:space_uuid>/history-table/', views.history_table, name='history_table'),
    path('spaces/<uuid:space_uuid>/update/', views.space_edit, name='space_edit'),
    path('spaces/<uuid:space_uuid>/all-senders-modal/', views.all_senders_modal, name='all_senders_modal'),
    path('spaces/<uuid:space_uuid>/invite-all-senders/', views.bulk_notify_invitation, name='bulk_notify_invitation'),
    path('spaces/<uuid:space_uuid>/notify-all-senders/', views.bulk_notify_deadline, name='bulk_notify_deadline'),
    path('requests/<uuid:request_uuid>/modal/', views.request_modal, name='request_modal'),
    path('requests/<uuid:request_uuid>/files/changes/', views.request_changes, name='request_changes'),
    path('requests/<uuid:request_uuid>/files/accept/', views.accept_all, name='accept_all'),
    path('requests/<uuid:request_uuid>/delete/', views.delete_request, name='request_delete'),
    path('spaces/<uuid:space_uuid>/senders-history-table/', views.history_table, name='sender_history_table'),
    path('spaces/<uuid:space_uuid>/senders/create-row/', views.sender_create_row, name='sender_create_row'),
    path('spaces/<uuid:space_uuid>/senders/create/', views.sender_create, name='sender_create'),
    path('senders/<uuid:sender_uuid>/modal/', views.sender_modal, name='sender_modal'),
    path('senders/<uuid:sender_uuid>/sender-info/', views.sender_info, name='sender_info'),
    path('senders/<uuid:sender_uuid>/sender-row/', views.sender_row, name='sender_row'),
    path('senders/<uuid:sender_uuid>/toggle-active/', views.toggle_sender_active, name='toggle_sender_active'),
    path('senders/<uuid:sender_uuid>/notify_deadline/', views.notify_deadline, name='notify_deadline'),
    path('senders/<uuid:sender_uuid>/notify_invitation/', views.notify_invitation, name='notify_invitation'),
    path('senders/sender-upload-notification/', views.sender_upload_notification, name='sender_upload_notification'),
    path('companies/<uuid:company_uuid>/update/', views.company_update, name='company_update'),
    path('organizations/<uuid:organization_uuid>/contacts/search/', views.search_contacts, name='search_contacts'),
    path('organizations/<uuid:organization_uuid>/contacts/create/modal/', views.contact_create_modal,
         name='contact_create_modal'),
    path('organizations/<uuid:organization_uuid>/contacts/create/', views.ContactCreateView.as_view(),
         name='contact_create'),
    path('organizations/create/', views.create_organization, name='create_organization'),
    path('organizations/create/modal/', views.create_organization_modal, name='create_organization_modal'),
]
