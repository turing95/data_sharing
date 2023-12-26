from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_POST
from web_app.models import UploadRequest
from web_app.forms import DetailRequestFormSet


@login_required
@require_POST
def delete_request(request, request_uuid):
    req = UploadRequest.objects.get(pk=request_uuid)
    space = req.space
    req.is_deleted = True
    req.save()
    space.refresh_from_db()

    requests = DetailRequestFormSet(None,
                                    instance=space,
                                    queryset=space.requests.filter(is_deleted=False).order_by('created_at'),
                                    form_kwargs={'access_token': request.custom_user.google_token.token})
    return render(
        request,
        'private/space/components/request_form.html',
        {'requests': requests, 'action': 'edit'}
    )
