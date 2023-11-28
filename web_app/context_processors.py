import config


def private_area_context(request):
    # Set private_area to True only if the user is authenticated
    return {'private_area': request.user.is_authenticated, 'config_data': config.get_js_config()}
