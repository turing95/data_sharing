from django.views.defaults import page_not_found, server_error


def custom_page_not_found(request):
    return page_not_found(request, None)


def custom_server_error(request):
    return server_error(request)
