class AuthPageMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['auth_page'] = True
        return context