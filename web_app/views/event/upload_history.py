from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import TemplateView

from web_app.mixins import SubscriptionMixin, SpaceMixin, SpaceSideBarMixin
from web_app.models import Space


class UploadHistoryListView(LoginRequiredMixin, SubscriptionMixin, SpaceMixin, SpaceSideBarMixin, TemplateView):
    template_name = 'private/space/detail/event/upload_history.html'


def history_table(request, space_uuid):
    space = Space.objects.get(pk=space_uuid)
    upload_events = space.events.all()
    show_sender = True
    show_request = True

    if request.method == 'POST':
        search_query = request.POST.get('search')
        if search_query:
            upload_events = upload_events.filter(
                Q(files__name__icontains=search_query) |
                Q(sender__email__icontains=search_query) |
                Q(request__title__icontains=search_query) |
                Q(files__original_name__icontains=search_query)
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
