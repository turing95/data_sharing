from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils import translation
from django.views.decorators.http import require_GET
from django.urls import reverse
from web_app.models import Space, Company
from django.shortcuts import get_object_or_404




@login_required
@require_GET
def space_create(request, organization_uuid):
    
    
    if not request.user.can_create_space:
        return redirect('create_checkout_session')

    company_uuid = request.GET.get('company_uuid', None)
    if company_uuid:
        company = get_object_or_404(Company, pk=company_uuid)
    else:
        company = None
    space = Space.objects.create(title=f'untitled ({company.name})',
                                user=request.user,
                                organization_id=organization_uuid,
                                locale=translation.get_language(),  
                                company=company)
    space.setup()
    return redirect(reverse('receiver_space_detail', kwargs={'space_uuid': space.pk}))
