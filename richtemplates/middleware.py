from django.http import HttpResponseForbidden
from richtemplates.views import handle403

class Http403Middleware(object):
    """
    Handles 403 errors.
    """
    def process_response(self, request, response):
        if isinstance(response, HttpResponseForbidden):
            return handle403(request)
        else:
            return response

