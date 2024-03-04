from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from web_app.mixins import SubscriptionMixin, SpaceMixin, SpaceSideBarMixin


class UploadHistoryListView(LoginRequiredMixin, SubscriptionMixin, SpaceMixin, SpaceSideBarMixin, TemplateView):
    template_name = 'private/space/detail/event/upload_history.html'
