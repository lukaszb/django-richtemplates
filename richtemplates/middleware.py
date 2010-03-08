from django.http import HttpResponseForbidden
from richtemplates.views import handle403

class Http403Middleware(object):
    """
    Handles 403 errors.
    """
    def process_response(self, request, response):
        if isinstance(response, HttpResponseForbidden):
            if request.POST:
                print request.POST
            if request.FILES:
                print request.FILES
            return handle403(request)
        else:
            return response

