from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse

from django.shortcuts import render
from utils.render_block import render_block_to_string
from django.contrib.postgres.search import SearchVector, SearchQuery, TrigramSimilarity

from django.views.decorators.http import require_POST, require_GET

from web_app.forms import FileSelectForm
from web_app.models import Space, Sender, UploadRequest, SenderEvent, File


@login_required
@require_POST
def toggle_space_public(request, space_uuid):
    space = Space.objects.get(pk=space_uuid)
    space.is_public = not space.is_public
    space.save()
    return HttpResponse(
        render_block_to_string('private/space/detail/components/summary.html', 'details', {'space': space}, request))


@login_required
def history_table(request, space_uuid):
    space = Space.objects.get(pk=space_uuid)
    upload_events = space.events.all()
    show_sender = True
    show_request = True

    if request.method == 'POST':
        search_query = request.POST.get('search')
        if search_query:
            upload_events = upload_events.annotate(
                name_similarity=TrigramSimilarity('files__name', search_query),
                email_similarity=TrigramSimilarity('sender__email', search_query),
                title_similarity=TrigramSimilarity('request__title', search_query),
                original_name_similarity=TrigramSimilarity('files__original_name', search_query),
            ).filter(
                Q(name_similarity__gt=0.1) |
                Q(email_similarity__gt=0.1) |
                Q(title_similarity__gt=0.1) |
                Q(original_name_similarity__gt=0.1)
            )

    if request.GET.get('sender_uuid'):
        sender_uuid = request.GET.get('sender_uuid')
        upload_events = upload_events.filter(sender__uuid=sender_uuid)
        show_sender = False

    if request.GET.get('request_uuid'):
        request_uuid = request.GET.get('request_uuid')
        upload_events = upload_events.filter(request__uuid=request_uuid)
        show_request = False
    if request.GET.get('public'):
        upload_events = upload_events.filter(sender__isnull=True)
        show_sender = False

    return render(request, 'private/space/detail/components/history_table.html',
                  {'space': space, 'upload_events': upload_events, 'show_request': show_request,
                   'show_sender': show_sender})


@login_required
@require_GET
def request_modal(request, request_uuid):
    upload_request = UploadRequest.objects.get(pk=request_uuid)

    sender = None
    public = False
    files = File.objects.filter(sender_event__request=upload_request)
    if request.GET.get('public'):
        public = True
        files = files.filter(sender_event__sender=None)
    elif request.GET.get('sender_uuid'):
        sender_uuid = request.GET.get('sender_uuid')
        sender = Sender.objects.get(pk=sender_uuid)
        files = files.filter(sender_event__sender=sender)
    changes_form = FileSelectForm(upload_request=upload_request, sender=sender,public=public)

    return render(request, 'private/space/detail/components/request_modal.html',
                  {'req': upload_request,
                   'sender': sender,
                   'files': files,
                   'public': public,
                   'changes_form': changes_form})
