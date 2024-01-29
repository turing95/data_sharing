from django.contrib.humanize.templatetags.humanize import intcomma
from djstripe.models import Product
from djstripe.utils import get_friendly_currency_amount, CURRENCY_SIGILS

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
    # TODO REMOVE - PICKER LEGACY
    #context['config_data'] = config.get_js_config()
    context['contact_email'] = settings.CONTACT_EMAIL
    context['pro_product'] = Product.objects.filter(name="Pro").first()
    if context['pro_product'] is not None:
        unit_amount = (context['pro_product'].default_price.unit_amount or 0) / 100
        sigil = CURRENCY_SIGILS.get(context['pro_product'].default_price.currency.upper(), "")
        amount_two_decimals = f"{unit_amount:.2f}"
        formatted_price = f"{sigil}{intcomma(amount_two_decimals)}"
        context['pro_product_formatted_price'] = formatted_price
        
    context['doc_url'] = settings.DOC_URL
    return context
