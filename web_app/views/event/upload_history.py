from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import TemplateView

from web_app.mixins import SubscriptionMixin, SpaceMixin, SpaceSideBarMixin
from web_app.models import Space
from web_app.views.space.detail import SpaceTabMixin


class HistoryListView(LoginRequiredMixin, SubscriptionMixin, SpaceMixin, SpaceSideBarMixin, SpaceTabMixin, TemplateView):
    template_name = 'private/space/detail/event/history.html'
    
    #set context space_tab to active
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['space_tab']['history']['active'] = True
        return context


def history_table(request, space_uuid):
    space = Space.objects.get(pk=space_uuid)
    events = space.events.all()
    show_sender = True
    show_request = True

    if request.method == 'POST':
        search_query = request.POST.get('search')
        if search_query:
            events = events.filter(
                Q(sender__email__icontains=search_query) |
                Q(upload_request__title__icontains=search_query) |
                Q(text_request__title__icontains=search_query) |
                Q(request__title__icontains=search_query) |
                Q(files__original_name__icontains=search_query)
            )
    if request.GET.get('sender_uuid'):
        sender_uuid = request.GET.get('sender_uuid')
        events = events.filter(sender__uuid=sender_uuid)
        show_sender = False

    if request.GET.get('request_uuid'):
        request_uuid = request.GET.get('request_uuid')
        events = events.filter(request__uuid=request_uuid)
        show_request = False

    return render(request, 'private/space/detail/components/history_table.html',
                  {'space': space, 'upload_events': events, 'show_request': show_request,
                   'show_sender': show_sender})
