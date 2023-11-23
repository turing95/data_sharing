from django.urls import path
from web_app.views import SpacesView, SpaceFormView, SpaceDetailFormViewSender, SpaceDetailFormViewReceiver

urlpatterns = [
    path('', SpacesView.as_view(), name='spaces'),
    path('spaces/add/', SpaceFormView.as_view(), name='space_create'),
    path('spaces/detail/<uuid:space_uuid>/', SpaceDetailFormViewReceiver.as_view(), name='receiver_space_detail'),
    path('spaces/<uuid:sender_uuid>/', SpaceDetailFormViewSender.as_view(), name='sender_space_detail')
]
