from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_GET
from web_app.models import Space, Request, InputRequest


@login_required
@require_GET
def request_create(request, space_uuid):
    space = get_object_or_404(Space, pk=space_uuid)
    space_request = Request.objects.create(space=space, title='Untitled')
    return redirect('request_detail', request_uuid=space_request.pk)


@require_GET
def request_create_nested(request, request_uuid):
    parent_request = get_object_or_404(Request, pk=request_uuid)
    nested_request = Request.objects.create(space=parent_request.space, request=parent_request, title='Untitled')
    parent_request.add_input_request(child_request=nested_request,
                                     prev_request_position=request.GET.get('input_request_position'))
    if request.headers.get('HX-Request'):
        response = HttpResponse()
        response['HX-Trigger'] = 'update_order'
        return response
    return redirect('request_detail', request_uuid=parent_request.pk)