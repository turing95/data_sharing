from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from web_app.models import FileType
import re


@login_required
def search_file_types(request):
    if request.method == 'POST':
        pattern = re.compile(r'search-file-types-\d+-')

        for key in request.POST.keys():
            if re.match(pattern, key):
                search_query = request.POST[key]
                break
        file_types = FileType.objects.filter(group=False)
        if search_query:
            file_types = file_types.filter(slug__icontains=search_query)

    return render(request,
                  'private/space/create/components/file_type_search_results.html',
                  {'file_types': file_types})
