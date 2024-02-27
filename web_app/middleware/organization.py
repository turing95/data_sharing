from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin

from web_app.models import Organization


class OrganizationMiddleware(MiddlewareMixin):
    """
    Parse a request and decide what organization object to install in the
    current thread context.
    """

    response_redirect_class = HttpResponseRedirect

    def process_request(self, request):
        if not hasattr(request, 'user'):
            raise Exception(
                "The OrganizationMiddleware requires authentication middleware to be installed. Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.auth.middleware.AuthenticationMiddleware'."
            )
        if request.user.is_authenticated:
            if request.session.get('organization_uuid',None) is None:
                try:
                    request.session['organization_uuid'] = str(request.user.created_organizations.get(name='Personal').pk)
                except Organization.DoesNotExist:
                    request.user.organization_set.update(created_by=request.user)
                    request.session['organization_uuid'] = str(request.user.created_organizations.get(name='Personal').pk)
