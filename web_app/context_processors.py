from djstripe.models import Product

import config
from django.conf import settings


def custom_context(request):
    context = {}
    context['generic_area'] = True
    if request.resolver_match is not None:
        url_name = request.resolver_match.url_name
        if url_name is not None:
            context['sender_area'] = True if 'sender' in url_name else False
            context['generic_area'] = True if 'generic' in url_name else False
    context['config_data'] = config.get_js_config()
    context['contact_email'] = settings.CONTACT_EMAIL
    context['pro_product'] = Product.objects.filter(name="Pro").first()
    return context
