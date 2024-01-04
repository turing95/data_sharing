import config


def private_area_context(request):
    # Set private_area to True only if the user is authenticated
    return {'private_area': request.user.is_authenticated, 'config_data': config.get_js_config()}

def account_pages_context(request):
    # Check if '/accounts/' is in the first part of the URL path
    if 'accounts' in request.path.split('/')[1]:
        return {'account_page': True}
    else:
        return {'account_page': False}
