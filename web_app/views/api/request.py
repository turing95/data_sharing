from django.shortcuts import render
from django.views.decorators.http import require_POST
from web_app.models import UploadRequest
from web_app.forms import DetailRequestFormSet


@require_POST
def delete_request(request, request_uuid):
    req = UploadRequest.objects.get(pk=request_uuid)
    req.is_deleted = True
    req.save()
    space = req.space
    print(space.requests.count())
    space.refresh_from_db()
    print(space.requests.count())

    requests = DetailRequestFormSet(None,
                                    instance=space,
                                    queryset=space.requests.order_by('created_at'),
                                    form_kwargs={'access_token': request.custom_user.google_token.token})
    return render(
        request,
        'private/space/components/request_form.html',
        {'requests': requests, 'action': 'edit'}
    )
