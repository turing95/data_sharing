from django.shortcuts import redirect
from django.views.decorators.http import require_GET


@require_GET
def cookie_policy(request):
    return redirect('https://www.iubenda.com/privacy-policy/54001192/cookie-policy/')