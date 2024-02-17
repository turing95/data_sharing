from django.conf import settings
from django.templatetags.static import static


def get_base_context_for_email():
    return {
        'contact_email': settings.CONTACT_EMAIL,
        'homepage_link': settings.BASE_URL,
        'logo_link': settings.BASE_URL + static('images/logo.png'),
    }
