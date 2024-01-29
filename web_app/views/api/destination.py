from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
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
        request_index = request.GET.get('request_index', None)
        if request_index is not None:
            search_query = request.POST.get(f'search-folders-{request_index}-')
            search_type = request.POST[f'requests-{request_index}-destination_type_select']
            if search_query == '':
                return HttpResponse(status=204)

            else:
                folders = request.custom_user.get_folders(search_type, search_query)
            return render(request,
                          'private/space/create/components/destination/folders_search_results.html',
                          {'folders': folders, 'destination_type': search_type})
    return HttpResponseBadRequest()


@login_required
@require_GET
def select_destination_type(request):
    if request.method == 'GET':
        custom_user = request.custom_user
        request_index = request.GET.get('request_index', None)
        if request_index is not None:
            missing_provider = None
            provider_type = request.GET.get(f'requests-{request_index}-destination_type_select')
            next_path = request.GET.get('next', None)
            if provider_type == GoogleDrive.TAG:
                if custom_user.google_account is None:
                    adapter = get_adapter()
                    missing_provider = adapter.get_provider(request, GoogleDrive.PROVIDER_ID)

            elif provider_type == OneDrive.TAG:
                if custom_user.microsoft_account is None:
                    adapter = get_adapter()
                    missing_provider = adapter.get_provider(request, OneDrive.PROVIDER_ID)
            else:
                return HttpResponseBadRequest()

            return render(request,
                          'private/space/create/components/destination/destination_search.html',
                          {
                              'missing_provider': missing_provider, 'next': next_path, 'request_index': request_index})
    return HttpResponseBadRequest()


@login_required
@require_GET
def get_destination_logo(request):
    if request.method == 'GET':
        return render(request,
               'private/space/create/components/destination/destination_logo.html',
               {'tag': request.GET.get('tag')})
    return HttpResponseBadRequest()
