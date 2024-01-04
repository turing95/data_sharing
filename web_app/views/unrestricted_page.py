
class UnrestrictedAccessMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unrestricted_access_page'] = True
        return context