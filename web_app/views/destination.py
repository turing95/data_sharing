from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import render
import re
from web_app.models import GoogleDrive, OneDrive, SharePoint, Kezyy
from allauth.socialaccount.adapter import get_adapter
from django.http import HttpResponseBadRequest  # Import HttpResponseBadRequest


@login_required
@require_POST
def search_folder_old(request):
    if request.method == 'POST':
        request_index = request.GET.get('request_index', None)

        if request_index is not None:
            search_query = request.POST.get(f'search-folders-{request_index}-')
            sharepoint_site_id = request.POST.get(f'sharepoint-site-{request_index}-', None)
            search_type = request.POST[f'requests-{request_index}-destination_type_select']
            if search_query == '':
                return HttpResponse('')

            else:
                folders = request.user.get_folders(search_type, search_query, sharepoint_site_id)
            return render(request,
                          'private/space/create/components/destination/folders_search_results.html',
                          {'folders': folders, 'destination_type': search_type,
                           'sharepoint_site_id': sharepoint_site_id})
    return HttpResponseBadRequest()


@login_required
@require_POST
def search_folder(request):
    if request.method == 'POST':
        search_query = request.POST.get(f'search-folders')
        sharepoint_site_id = request.POST.get(f'sharepoint-site', None)
        search_type = request.POST['destination_type_select']
        if search_query == '':
            return HttpResponse('')
        else:
            folders = request.user.get_folders(search_type, search_query, sharepoint_site_id)
        return render(request,
                      'private/space/create/components/destination/folders_search_results.html',
                      {'folders': folders, 'destination_type': search_type,
                       'sharepoint_site_id': sharepoint_site_id})
    return HttpResponseBadRequest()


@login_required
@require_GET
def select_destination_type_old(request):
    if request.method == 'GET':
        request_index = request.GET.get('request_index', None)
        if request_index is not None:
            missing_provider = None
            expired_provider = None
            account = None
            provider_type = request.GET.get(f'requests-{request_index}-destination_type_select')
            next_path = request.GET.get('next', None)
            adapter = get_adapter()
            if provider_type == GoogleDrive.TAG:
                provider_name = "Google Drive"
                if request.user.google_account is None:
                    missing_provider = adapter.get_provider(request, GoogleDrive.PROVIDER_ID)
                elif request.user.google_account.socialtoken_set.count() == 0:
                    account = request.user.google_account
                    expired_provider = adapter.get_provider(request, GoogleDrive.PROVIDER_ID)

            elif provider_type == OneDrive.TAG:
                provider_name = "OneDrive"
                if request.user.microsoft_account is None:
                    missing_provider = adapter.get_provider(request, OneDrive.PROVIDER_ID)
                elif request.user.microsoft_account.socialtoken_set.count() == 0:
                    account = request.user.microsoft_account

                    expired_provider = adapter.get_provider(request, OneDrive.PROVIDER_ID)
            elif provider_type == SharePoint.TAG:
                provider_name = "SharePoint"
                if request.user.microsoft_account is None:
                    account = request.user.microsoft_account
                    missing_provider = adapter.get_provider(request, SharePoint.PROVIDER_ID)
                elif request.user.microsoft_account.socialtoken_set.count() == 0:
                    expired_provider = adapter.get_provider(request, SharePoint.PROVIDER_ID)
            elif provider_type == Kezyy.TAG:
                provider_name = "Kezyy"
            else:
                return HttpResponseBadRequest()

            return render(request,
                          'private/space/create/components/destination/destination_search.html',
                          {
                              'missing_provider': missing_provider, 'expired_provider': expired_provider,
                              'next': next_path, 'account': account, 'request_index': request_index,
                              'provider_name': provider_name, 'from_htmx': True})
    return HttpResponseBadRequest()

@login_required
@require_GET
def select_destination_type(request):
    if request.method == 'GET':
        missing_provider = None
        expired_provider = None
        account = None
        provider_type = request.GET.get(f'destination_type_select')
        next_path = request.GET.get('next', None)
        adapter = get_adapter()
        if provider_type == GoogleDrive.TAG:
            provider_name = "Google Drive"
            if request.user.google_account is None:
                missing_provider = adapter.get_provider(request, GoogleDrive.PROVIDER_ID)
            elif request.user.google_account.socialtoken_set.count() == 0:
                account = request.user.google_account
                expired_provider = adapter.get_provider(request, GoogleDrive.PROVIDER_ID)

        elif provider_type == OneDrive.TAG:
            provider_name = "OneDrive"
            if request.user.microsoft_account is None:
                missing_provider = adapter.get_provider(request, OneDrive.PROVIDER_ID)
            elif request.user.microsoft_account.socialtoken_set.count() == 0:
                account = request.user.microsoft_account

                expired_provider = adapter.get_provider(request, OneDrive.PROVIDER_ID)
        elif provider_type == SharePoint.TAG:
            provider_name = "SharePoint"
            if request.user.microsoft_account is None:
                account = request.user.microsoft_account
                missing_provider = adapter.get_provider(request, SharePoint.PROVIDER_ID)
            elif request.user.microsoft_account.socialtoken_set.count() == 0:
                expired_provider = adapter.get_provider(request, SharePoint.PROVIDER_ID)
        elif provider_type == Kezyy.TAG:
            provider_name = "Kezyy"
        else:
            return HttpResponseBadRequest()

        return render(request,
                      'private/space/create/components/destination/destination_search.html',
                      {
                          'missing_provider': missing_provider, 'expired_provider': expired_provider,
                          'next': next_path, 'account': account, 'provider_name': provider_name, 'from_htmx': True})
    return HttpResponseBadRequest()

@login_required
def get_destination_logo_old(request):
    if request.method == 'GET':
        return render(request,
                      'private/space/create/components/destination/destination_logo.html',
                      {'tag': request.GET.get('tag')})
    elif request.method == 'POST':
        request_index = request.GET.get('request_index', None)
        return render(request,
                      'private/space/create/components/destination/destination_logo.html',
                      {'tag': request.POST[f'requests-{request_index}-destination_type']})
    return HttpResponseBadRequest()


@login_required
def get_destination_logo(request):
    if request.method == 'GET':
        return render(request,
                      'private/space/create/components/destination/destination_logo.html',
                      {'tag': request.GET.get('tag')})
    elif request.method == 'POST':
        return render(request,
                      'private/space/create/components/destination/destination_logo.html',
                      {'tag': request.POST[f'destination_type']})
    return HttpResponseBadRequest()