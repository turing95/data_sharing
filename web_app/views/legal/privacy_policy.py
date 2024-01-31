from django.shortcuts import redirect
from django.views.decorators.http import require_GET


@require_GET
def privacy_policy(request):
    return redirect('https://www.iubenda.com/privacy-policy/54001192/')