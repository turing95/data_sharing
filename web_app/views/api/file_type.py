from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from web_app.models import FileType
import re


@login_required
def search_file_types(request):
    if request.method == 'POST':
        request_index = request.GET.get('request_index', None)
        if request_index is not None:
            search_query = request.POST.get(f'search-file-types-{request_index}-', '')
            file_types = FileType.objects.filter(group=False)
            if search_query:
                file_types = file_types.filter(slug__icontains=search_query)

            return render(request,
                          'private/space/create/components/file_type_search_results.html',
                          {'file_types': file_types})
    return HttpResponseBadRequest()

