from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import render
import re
from web_app.models import GoogleDrive, OneDrive
from allauth.socialaccount.adapter import get_adapter
from django.http import HttpResponseBadRequest  # Import HttpResponseBadRequest


@login_required
@require_POST
def search_folder(request):
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
        if search_query == '':
            folders = None
        else:
            folders = request.custom_user.get_folders(search_type, search_query)
        return render(request,
                      'private/space/create/components/folders_search_results.html',
                      {'folders': folders, 'destination_type': search_type})
    return HttpResponseBadRequest()


@login_required
@require_GET
def select_destination_type(request):
    if request.method == 'GET':
        request_index = request.GET.get('request_index', None)
        custom_user = request.custom_user
        type_pattern = re.compile(r'.*destination_type_select.*')
        provider_available = False
        missing_provider = None
        provider_type = None

        for key in request.GET.keys():
            if re.match(type_pattern, key):
                provider_type = request.GET[key]
                break
        next_path = request.GET.get('next', None)
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
        else:
            return HttpResponseBadRequest()

        return render(request,
                      'private/space/create/components/destination_search.html',
                      {'provider_available': provider_available,
                       'missing_provider': missing_provider, 'next': next_path, 'request_index': request_index})
    return HttpResponseBadRequest()
