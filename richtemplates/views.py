from django.http import HttpResponseForbidden, Http404
from django.views.generic.simple import direct_to_template
from django.shortcuts import redirect, get_object_or_404, render_to_response
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.contrib import messages
from django.template import RequestContext
from django.core.exceptions import PermissionDenied

from richtemplates import settings as richtemplates_settings
from richtemplates.skins import set_skin_at_request, SkinDoesNotExist
from richtemplates.forms import UserProfileForm

def handle403(request, template_name='403.html'):
    """
    Default error 403 (Permission denied) handler.
    """

    response = direct_to_template(request, template=template_name)
    response.status_code = 403
    return response


