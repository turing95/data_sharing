from django.urls import path, re_path
from web_app import views

urlpatterns = [
    # Generic views
    path('accounts/set-language/', views.custom_set_language, name='set_user_language'),
    path('accounts/language-modal/', views.language_modal, name='language_modal'),
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
    path('sender-notifications-settings/<uuid:notifications_settings_uuid>/',
         views.sender_notifications_settings_update,
         name='sender_notifications_settings_update'),
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
    path('organizations/<uuid:organization_uuid>/grants/', views.GrantListView.as_view(), name='grants'),
    path('organizations/<uuid:organization_uuid>/grants/create/', views.grant_create, name='grant_create'),
    path('grants/<uuid:grant_uuid>/detail/', views.GrantDetailView.as_view(), name='grant_detail'),
    path('grants/<uuid:grant_uuid>/checklist/', views.GrantChecklistView.as_view(), name='grant_checklist'),
    path('grants/<uuid:grant_uuid>/edit/', views.GrantEditView.as_view(), name='grant_edit'),
    path('grants/<uuid:grant_uuid>/delete/', views.GrantDeleteView.as_view(), name='grant_delete'),
    path('grants/<uuid:grant_uuid>/update/', views.grant_update, name='grant_update'),
    path('grants/<uuid:grant_uuid>/update-name/', views.grant_update_name, name='grant_update_name'),
    path('companies/<uuid:company_uuid>/detail/', views.CompanyDetailView.as_view(), name='company_detail'),
    path('companies/<uuid:company_uuid>/delete/', views.CompanyDeleteView.as_view(), name='company_delete'),
    path('companies/<uuid:company_uuid>/spaces/', views.CompanySpacesListView.as_view(), name='company_spaces'),
    path('companies/<uuid:company_uuid>/contacts/', views.CompanyContactsListView.as_view(), name='company_contacts'),
    path('companies/<uuid:company_uuid>/files/', views.CompanyFilesListView.as_view(), name='company_files'),
    path('field-group-templates/<uuid:template_uuid>/', views.FieldGroupTemplateDetailView.as_view(),
         name='company_template_detail'),
    path('company-templates/<uuid:company_template_uuid>/delete/', views.FieldGroupTemplateDeleteView.as_view(),
         name='company_template_delete'),
    path('organizations/<uuid:organization_uuid>/company-templates/', views.FieldGroupTemplatesListView.as_view(),
         name='company_templates'),
    path('field-groups/<uuid:group_uuid>/company-templates/search/', views.search_templates,
         name='company_templates_search'),
    path('organizations/<uuid:organization_uuid>/contacts/', views.ContactListView.as_view(), name='contacts'),
    path('organizations/<uuid:organization_uuid>/delete/', views.OrganizationDeleteView.as_view(),
         name='organization_delete'),
    path('organizations/<uuid:organization_uuid>/update/', views.organization_update, name='organization_update'),
    path('spaces/<uuid:space_uuid>/detail/', views.SpaceRequestsView.as_view(), name='receiver_space_detail'),
    path('spaces/<uuid:space_uuid>/documents/', views.SpaceDocumentsView.as_view(), name='space_documents'),
    path('spaces/<uuid:space_uuid>/settings/', views.SpaceSettingsView.as_view(), name='space_settings'),
    path('spaces/<uuid:space_uuid>/history/', views.HistoryListView.as_view(), name='space_history'),
    path('spaces/<uuid:space_uuid>/content/', views.SpaceContentView.as_view(), name='space_content'),
    path('spaces/<uuid:space_uuid>/senders/', views.SenderListView.as_view(), name='senders'),
    path('spaces/<uuid:space_uuid>/requests/create/', views.request_create, name='request_create'),
    path('requests/<uuid:request_uuid>/create/nested/', views.request_create_nested, name='request_create_nested'),
    path('requests/<uuid:request_uuid>/detail/', views.RequestDetailView.as_view(), name='request_detail'),
    path('requests/<uuid:request_uuid>/edit/', views.RequestEditView.as_view(), name='request_edit'),
    path('requests/<uuid:request_uuid>/update/title/', views.request_title_update, name='request_title_update'),
    path('requests/<uuid:request_uuid>/update/instructions/', views.request_instructions_update,
         name='request_instructions_update'),
    path('requests/<uuid:request_uuid>/update-order/', views.request_update_order, name='request_update_order'),
    path('requests/<uuid:request_uuid>/input-requests/', views.input_requests, name='input_requests'),
    path('spaces/<uuid:space_uuid>/update-order/', views.space_section_update_order, name='space_section_update_order'),
    path('spaces/<uuid:space_uuid>/sections/', views.sections, name='sections'),
    path('requests/<uuid:request_uuid>/upload-requests/create/', views.upload_request_create,
         name='upload_request_create'),
    path('upload-requests/<uuid:upload_request_uuid>/update/', views.upload_request_update,
         name='upload_request_update'),
    path('input-requests/<uuid:input_request_uuid>/update-active/', views.input_request_update_active,
         name='input_request_update_active'),
    path('input-requests/<uuid:input_request_uuid>/delete/', views.input_request_delete, name='input_request_delete'),
    path('input-requests/<uuid:input_request_uuid>/update-complete/', views.input_request_update_complete,
         name='input_request_update_complete'),
    path('input-requests/<uuid:input_request_uuid>/detail-show/', views.input_request_detail_show,
         name='input_request_detail_show'),
    path('outputs/<uuid:output_uuid>/accept/', views.output_accept,
         name='output_accept'),
    path('outputs/<uuid:output_uuid>/reject/', views.output_reject,
         name='output_reject'),
    path('outputs/<uuid:output_uuid>/reject-modal/', views.output_reject_modal,
         name='output_reject_modal'),
    path('outputs/<uuid:output_uuid>/detail/', views.output_detail,
         name='output_detail'),
    path('upload-requests/<uuid:upload_request_uuid>/detail-show/', views.upload_request_detail_show,
         name='upload_request_detail_show'),
    path('requests/<uuid:request_uuid>/text-requests/create/', views.text_request_create, name='text_request_create'),
    path('spaces/<uuid:space_uuid>/text-sections/create/', views.text_section_create, name='text_section_create'),
    path('spaces/<uuid:space_uuid>/file-sections/create/', views.file_section_create, name='file_section_create'),
    path('text-requests/<uuid:text_request_uuid>/update/', views.text_request_update,
         name='text_request_update'),
    path('text-sections/<uuid:section_uuid>/update/', views.text_section_update,
         name='text_section_update'),
    path('file-sections/<uuid:file_section_uuid>/update/', views.file_section_update,
         name='file_section_update'),
    path('space-sections/<uuid:space_section_uuid>/delete/', views.section_delete, name='section_delete'),
    path('organizations/<uuid:organization_uuid>/team/', views.TeamView.as_view(), name='team'),
    path('organizations/<uuid:organization_uuid>/team-invitation/', views.team_invitation, name='team_invitation'),
    path('organizations/<uuid:organization_uuid>/settings/', views.OrganizationSettingsView.as_view(),
         name='organization_settings'),
    path('team-invitation-redemption/', views.team_invitation_redemption, name='team_invitation_redemption'),
    path('<uuid:invitation_uuid>/revoke-invitation/', views.revoke_invitation, name='revoke_invitation'),
    path('<uuid:user_org_uuid>/delete/', views.remove_team_member, name='remove_team_member'),
    path('spaces/delete/<uuid:space_uuid>/', views.DeleteSpaceView.as_view(), name='space_delete'),
    path('spaces/duplicate/<uuid:space_uuid>/', views.duplicate, name='space_duplicate'),
    path('stripe/create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('stripe/create-billing-session/', views.create_billing_session, name='create_billing_session'),
    path('senders/<uuid:sender_uuid>/spaces/<uuid:space_uuid>/', views.SpaceDetailFormViewSender.as_view(),
         name='sender_space_detail'),
    path('senders/<uuid:sender_uuid>/spaces/<uuid:space_uuid>/requests/', views.RequestListViewSender.as_view(),
         name='sender_space_requests'),
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
    path('spaces/<uuid:space_uuid>/update/', views.space_update, name='space_update'),
    path('requests/<uuid:request_uuid>/files/changes/', views.request_changes, name='request_changes'),
    path('requests/<uuid:request_uuid>/files/accept/', views.accept_all, name='accept_all'),
    path('spaces/<uuid:space_uuid>/senders-history-table/', views.history_table, name='sender_history_table'),
    path('spaces/<uuid:space_uuid>/senders/create-row/', views.sender_create_row, name='sender_create_row'),
    path('senders/<uuid:sender_uuid>/contact-update/', views.sender_contact_update, name='sender_contact_update'),
    path('senders/<uuid:sender_uuid>/notify/', views.sender_notify, name='sender_notify'),
    path('senders/<uuid:sender_uuid>/sender-row/', views.sender_row, name='sender_row'),
    path('senders/<uuid:sender_uuid>/toggle-active/', views.toggle_sender_active, name='toggle_sender_active'),
    path('senders/<uuid:sender_uuid>/notify_deadline/', views.notify_deadline, name='notify_deadline'),
    path('senders/<uuid:sender_uuid>/notify_invitation/', views.notify_invitation, name='notify_invitation'),
    path('senders/sender-upload-notification/', views.sender_upload_notification, name='sender_upload_notification'),
    path('companies/<uuid:company_uuid>/update-name/', views.company_update_name, name='company_update_name'),
    path('companies/<uuid:company_uuid>/to-space/', views.company_to_space, name='company_to_space'),
    path('senders/<uuid:sender_uuid>/notify-modal/', views.sender_notify_modal, name='sender_notify_modal'),
    path('companies/<uuid:company_uuid>/update/', views.company_update, name='company_update'),
    path('field-groups/<uuid:group_uuid>/text-fields/create/', views.text_field_create,
         name='text_field_create'),
    path('field-groups/<uuid:group_uuid>/file-fields/create/', views.file_field_create,
         name='file_field_create'),
    path('field-groups/<uuid:group_uuid>/add-template/<uuid:template_uuid>/', views.field_group_add_template,
         name='field_group_add_template'),
    path('field-groups/<uuid:group_uuid>/to-template/', views.field_group_to_template,
         name='field_group_to_template'),
    path('field-groups/<uuid:group_uuid>/text-field/create/modal/', views.text_field_create_modal,
         name='text_field_create_modal'),
    path('field-groups/<uuid:group_uuid>/file-field/create/modal/', views.file_field_create_modal,
         name='file_field_create_modal'),
    path('field-groups/<uuid:group_uuid>/company-field-group/create/modal/', views.field_group_create_modal,
         name='field_group_create_modal'),
    path('field-groups/<uuid:group_uuid>/company-field-group/create/', views.field_group_create,
         name='field_group_create'),
    path('text-fields/<uuid:field_uuid>/update/modal/', views.text_field_update_modal,
         name='text_field_update_modal'),
    path('text-fields/<uuid:field_uuid>/duplicate/', views.text_field_duplicate,
         name='text_field_duplicate'),
    path('file-fields/<uuid:field_uuid>/update/modal/', views.file_field_update_modal,
         name='file_field_update_modal'),
    path('file-fields/<uuid:field_uuid>/duplicate/', views.file_field_duplicate,
         name='file_field_duplicate'),
    path('field-groups/<uuid:group_uuid>/elements/', views.group_elements,
         name='group_elements'),
    path('field-groups/<uuid:group_uuid>/update-order/', views.group_elements_update_order,
         name='group_elements_update_order'),
    path('field-groups/<uuid:group_uuid>/update/modal/', views.field_group_create_modal,
         name='field_group_update_modal'),
    path('field-groups/<uuid:group_uuid>/update/', views.field_group_update,
         name='field_group_update'),
    path('text-fields/<uuid:field_uuid>/update/', views.text_field_update, name='text_field_update'),
    path('file-fields/<uuid:field_uuid>/update/', views.file_field_update, name='file_field_update'),
    path('text-fields/<uuid:field_uuid>/detail/', views.text_field_detail,
         name='text_field_detail'),
    path('file-fields/<uuid:field_uuid>/detail/', views.file_field_detail,
         name='file_field_detail'),
    path('text-fields/<uuid:field_uuid>/delete/', views.text_field_delete, name='text_field_delete'),
    path('file-fields/<uuid:field_uuid>/delete/', views.file_field_delete, name='file_field_delete'),
    path('field-groups/<uuid:group_uuid>/delete/', views.field_group_delete, name='field_group_delete'),
    path('text-fields/<uuid:field_uuid>/update-value/', views.text_field_update_value,
         name='text_field_update_value'),
    path('file-fields/<uuid:field_uuid>/update-value/', views.file_field_update_value,
         name='file_field_update_value'),
    path('organizations/<uuid:organization_uuid>/contacts/search/', views.search_contacts, name='search_contacts'),
    path('organizations/<uuid:organization_uuid>/contacts/create/modal/', views.contact_create_modal,
         name='contact_create_modal'),
    path('organizations/<uuid:organization_uuid>/contacts/create/', views.ContactCreateView.as_view(),
         name='contact_create'),
    path('contacts/<uuid:contact_uuid>/delete/', views.DeleteContactView.as_view(), name='contact_delete'),
    path('contacts/<uuid:contact_uuid>/detail/', views.ContactDetailView.as_view(), name='contact_detail'),
    path('organizations/create/', views.create_organization, name='create_organization'),
    path('organizations/create/modal/', views.create_organization_modal, name='create_organization_modal'),
]
