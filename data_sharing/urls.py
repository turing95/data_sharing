"""
URL configuration for data_sharing project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from web_app.urls import urlpatterns
urlpatterns = [
    path('50870454-admin/', admin.site.urls),
    path("", include(urlpatterns)),
    path('accounts/', include('allauth.urls')),
    path("stripe/", include("djstripe.urls", namespace="djstripe")),
    path('i18n/', include('django.conf.urls.i18n'))

]
