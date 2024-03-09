from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST, require_GET
# import GET from django


from web_app.models import Request, InputRequest, TextRequest


@login_required
@require_GET
def text_request_create(request, request_uuid): 
    space_request = get_object_or_404(Request, pk=request_uuid)
    text_request = TextRequest.objects.create(request=space_request)

    input_request_uuid = request.GET.get('input_request_uuid')
    if input_request_uuid:
        
        current_input_request = get_object_or_404(InputRequest, pk=input_request_uuid)
        position = current_input_request.position+1
    else:
        position = 1
    space_request.update_positions_pre_addition(inserting_position=position)
    input_request = InputRequest.objects.create(request=space_request, text_request=text_request,position=position)
    
    if request.headers.get('HX-Request'):
        return render(request,
                      'private/request/input_request.html',
                      {'input_request': input_request,
                       'data_position': position,
                       'kezyy_request': space_request }
                      )
    return redirect('request_detail', request_uuid=space_request.pk)
