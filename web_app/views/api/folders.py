from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import render
import re
from web_app.models import GoogleDrive, OneDrive
from allauth.socialaccount.adapter import get_adapter


@login_required
@require_POST
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
        folders = request.custom_user.get_folders(search_type, search_query)
    return render(request,
                  'private/space/create/components/folders_search_results.html',
                  {'folders': folders, 'destination_type': search_type})


@login_required
@require_POST
def select_destination_type(request):
    if request.method == 'POST':
        custom_user = request.custom_user
        type_pattern = re.compile(r'.*destination_type_select.*')

        for key in request.POST.keys():
            if re.match(type_pattern, key):
                provider_type = request.POST[key]
                break

        provider_available = False
        missing_provider = None
        if provider_type == GoogleDrive.TAG:
            if custom_user.google_account:
                provider_available = True
            else:
                adapter = get_adapter()
                missing_provider = adapter.get_provider(request, GoogleDrive.PROVIDER_ID)

        elif provider_type == OneDrive.TAG:
            if custom_user.microsoft_account is not None:
                provider_available = True
            else:
                adapter = get_adapter()
                missing_provider = adapter.get_provider(request, OneDrive.PROVIDER_ID)

        return render(request,
                      'private/space/create/components/destination_search.html',
                      {'provider_available': provider_available,
                       'missing_provider': missing_provider, })
    raise Http404()
