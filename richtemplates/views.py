from django.http import HttpResponseForbidden, Http404
from django.views.generic.simple import direct_to_template
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from django.contrib import messages

from richtemplates import settings as richtemplates_settings
from richtemplates.skins import set_skin_at_request

def handle403(request, template_name='403.html'):
    """
    Default error 403 (Permission denied) handler.
    """

    response = direct_to_template(request, template=template_name)
    response.status_code = 403
    return response

def set_skin(request, skin):
    message = _("Skin set to %s" % skin)
    messages.info(request, message)
    set_skin_at_request(request, skin)
    return redirect('/')

