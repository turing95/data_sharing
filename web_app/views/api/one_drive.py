from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import re


@login_required
def search_one_drive(request):
    folders = None
    if request.method == 'POST':
        search_query = None
        pattern = re.compile(r'search-one-drive-\d+-')

        for key in request.POST.keys():
            if re.match(pattern, key):
                search_query = request.POST[key]
                break
        folders = request.custom_user.get_one_drive_folders(search_query)

    return render(request,
                  'private/space/create/components/one_drive_search_results.html',
                  {'folders': folders})
