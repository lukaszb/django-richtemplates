from django.http import HttpResponseForbidden, Http404
from django.views.generic.simple import direct_to_template
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from django.contrib import messages

def handle403(request, template_name='403.html'):
    """
    Default error 403 (Permission denied) handler.
    """

    response = direct_to_template(request, template=template_name)
    response.status_code = 403
    return response

def set_skin(request, skin_name):
    SKINS = ('aqua', 'ruby', 'django')
    if skin_name in SKINS:
        request.session['richtemplates_skin'] = skin_name
        message = _("Skin changed to %s" % skin_name)
        messages.info(request, message)
    else:
        message = _("There is no skin %s" % skin_name)
        messages.error(request, message)
    return redirect('/')

