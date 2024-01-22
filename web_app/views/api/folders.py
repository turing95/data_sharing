from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import re


@login_required
def search_folder(request):
    folders = None
    if request.method == 'POST':
        search_query = None
        search_type = None
        search_pattern = re.compile(r'search-folders-\d+-')
        type_pattern = re.compile(r'.*destination_type.*')

        for key in request.POST.keys():
            if re.match(search_pattern, key):
                search_query = request.POST[key]
            elif re.match(type_pattern, key):
                search_type = request.POST[key]
        folders = request.custom_user.get_folders(search_type,search_query)

    return render(request,
                  'private/space/create/components/one_drive_search_results.html',
                  {'folders': folders})
