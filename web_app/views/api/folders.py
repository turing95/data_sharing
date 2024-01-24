from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.shortcuts import render
from django.conf import settings
import re
from web_app.models import GoogleDrive, OneDrive
from allauth.socialaccount.adapter import get_adapter


@login_required
def search_folder(request):
    folders = None
    if request.method == 'POST':
        search_query = None
        search_type = None
        search_pattern = re.compile(r'search-folders-\d+-')
        type_pattern = re.compile(r'.*destination_type_select.*')

        for key in request.POST.keys():
            if re.match(search_pattern, key):
                search_query = request.POST[key]
            elif re.match(type_pattern, key):
                search_type = request.POST[key]
        folders = request.custom_user.get_folders(search_type,search_query)
    return render(request,
                  'private/space/create/components/folders_search_results.html',
                  {'folders': folders,'destination_type':search_type})

@login_required
@require_GET
def selected_provider(request):
    custom_user = request.custom_user
    type_pattern = re.compile(r'.*destination_type_select.*')

    for key in request.GET.keys():
        if re.match(type_pattern, key):
            provider_type = request.GET[key]
            break
        
    provider_available=False
    missing_provider=None
    provider_name=None
    service_name=None
    if provider_type == GoogleDrive.TAG:
        if custom_user.google_account:
            provider_available=True
        else:
            adapter= get_adapter()
            missing_provider = adapter.get_provider(request,GoogleDrive.PROVIDER_ID)
            provider_name = GoogleDrive.PROVIDER_SLAG
            service_name = GoogleDrive.SLAG
            
    elif provider_type == OneDrive.TAG:
        if custom_user.microsoft_account is not None:
            provider_available=True
        else:
            adapter= get_adapter()
            missing_provider = adapter.get_provider(request,OneDrive.PROVIDER_ID)
            provider_name = OneDrive.PROVIDER_SLAG
            service_name = OneDrive.SLAG
    
    return render(request,
                  'private/space/create/components/destination_search.html',
                  {'provider_available': provider_available,
                   'missing_provider': missing_provider,
                   'provider_name':provider_name,
                   'service_name':service_name,
                   'provider_name':provider_name })
