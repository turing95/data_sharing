from web_app.models import CustomUser


class CustomUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Attach custom_user to request
        if request.user.is_authenticated:
            request.custom_user = CustomUser.objects.get(pk=request.user.pk)
        else:
            request.custom_user = None

        response = self.get_response(request)
        return response
