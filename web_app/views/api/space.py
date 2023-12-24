from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from utils.render_block import render_block_to_string
from web_app.models import Space, SenderEvent
from django.contrib.postgres.search import SearchVector, SearchQuery, TrigramSimilarity


@require_POST
def toggle_space_active(request, space_uuid):
    space = Space.objects.get(pk=space_uuid)
    space.is_active = not space.is_active
    space.save()
    return HttpResponse(
        render_block_to_string('private/space/detail/components/summary.html', 'details', {'space': space}, request))


@require_POST
def toggle_space_public(request, space_uuid):
    space = Space.objects.get(pk=space_uuid)
    space.is_public = not space.is_public
    space.save()
    return HttpResponse(
        render_block_to_string('private/space/detail/components/summary.html', 'details', {'space': space}, request))


def history_table(request, space_uuid):
    space = Space.objects.get(pk=space_uuid)
    if request.method == 'GET':
        upload_events = space.upload_events
    elif request.method == 'POST':
        search_query = request.POST.get('search')
        upload_events = space.upload_events
        if search_query:
            search_query = request.POST.get('search')
            upload_events = upload_events.annotate(
                name_similarity=TrigramSimilarity('file__name', search_query),
                email_similarity=TrigramSimilarity('sender__email', search_query),
                title_similarity=TrigramSimilarity('request__title', search_query),
                original_name_similarity=TrigramSimilarity('file__original_name', search_query),
            ).filter(
                Q(name_similarity__gt=0.1) |
                Q(email_similarity__gt=0.1) |
                Q(title_similarity__gt=0.1) |
                Q(original_name_similarity__gt=0.1)
            )

    return render(request, 'private/space/detail/components/history_table.html',
                  {'space': space, 'upload_events': upload_events})
