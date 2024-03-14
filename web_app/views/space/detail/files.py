from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, TemplateView
from web_app.mixins import SubscriptionMixin, SpaceMixin, SpaceSideBarMixin, SpaceTabMixin
from web_app.models import File


class SpaceDocumentsView(LoginRequiredMixin, SubscriptionMixin, SpaceMixin, SpaceSideBarMixin, SpaceTabMixin,
                         TemplateView):
    template_name = "private/company/detail/files.html"
    model = File
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        return File.objects.filter(space=self.get_space())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['space_tab']['documents']['active'] = True
        return context
