from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.http import require_POST
from web_app.forms.widgets import ToggleWidget
from web_app.models import InputRequest
from django.contrib import messages
from django.utils.translation import gettext as _


@login_required
@require_POST
def input_request_update_active(request, input_request_uuid):
    if request.method == 'POST':
        input_request = get_object_or_404(InputRequest, pk=input_request_uuid)
        if input_request.upload_request:
            if input_request.upload_request.active_destination:
                input_request.is_active = not input_request.is_active
                input_request.save()
            else:
                
                messages.error(request,_("Please select a destination before activating the input"))
                
        elif input_request.text_request:
            input_request.is_active = not input_request.is_active
            input_request.save()
            
        # Get the initial context from ToggleWidget().get_context
        context = ToggleWidget().get_context('input_request_active_toggle', input_request.is_active, {
            'hx-post': reverse('input_request_update_active', kwargs={'input_request_uuid': input_request.pk}),
            'hx-trigger': "click", 
            'hx-swap': 'outerHTML', 
            'hx-target':'closest .toggle-container'
        })
        context.update({'from_htmx': True, 'show_msg': True})

        return render(request, 'forms/widgets/toggle.html', context)
    
    return HttpResponseBadRequest()


@login_required
@require_POST
def input_request_update_complete(request, input_request_uuid):
    if request.method == 'POST':
        input_request = get_object_or_404(InputRequest, pk=input_request_uuid)
        input_request.is_complete = not input_request.is_complete
        input_request.save()
        return HttpResponse()
    return HttpResponseBadRequest()



