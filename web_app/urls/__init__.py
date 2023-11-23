from django.urls import path
from web_app.views import SpacesView, SpaceFormView, SpaceDetailFormView
urlpatterns = [
    path('', SpacesView.as_view(), name='spaces'),
    path('spaces/add/', SpaceFormView.as_view(), name='space_create'),
    path('spaces/<uuid:recipient_uuid>/', SpaceDetailFormView.as_view(), name='space_detail')
]
