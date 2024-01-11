import config
from django.conf import settings

def custom_context(request):
    url_name = request.resolver_match.url_name
    context = {}
    if url_name is not None:
        context['sender_area'] = True if 'sender' in url_name else False
        context['generic_area'] = True if 'generic' in url_name else False
    context['config_data'] = config.get_js_config()
    context['contact_email']= ''.join(f'&#{ord(char)};' for char in settings.CONTACT_EMAIL)
    return context
