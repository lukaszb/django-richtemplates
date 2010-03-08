from django.http import HttpResponseForbidden
from django.views.generic.simple import direct_to_template

def handle403(request, template_name='403.html'):
    """
    Default error 403 (Permission denied) handler.
    """

    response = direct_to_template(request, template=template_name)
    response.status_code = 403
    return response
