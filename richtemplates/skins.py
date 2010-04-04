import logging
import richtemplates.settings

from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.db import models

from richtemplates.utils import get_user_profile_model
from pprint import pformat

class WrongSkinAlias(Exception): pass

class SkinDoesNotExist(Exception): pass

class RichSkin(object):
    def __init__(self, alias, name=None, url=None):
        if alias != slugify(alias):
            raise WrongSkinAlias("RichSkin's alias should be a slug "
                "('%s' is not a slug)" % alias)
        self.alias = alias
        if name is None:
            self.name = alias
        else:
            self.name = name
        if url is None:
            self.url = '%scss/skins/%s.css' %\
                (richtemplates.settings.MEDIA_URL, self.alias)
        else:
            self.url = url

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return unicode(self.name)

def get_skins_from_dict(skins_dict):
    """
    Returns list of RichSkin objects for the given dict.
    Keys of the ``skins_dict`` would be skins' aliases and
    values of the dict should be a dict with optional ``name``
    and ``url`` keys.
    Example:

    skins_dict = {
        'myskin': {'name': 'Some custom skin',
        'another-skin': {'url': 'path/file.css',
    }
    """
    return [RichSkin(alias, **info) for alias, info in skins_dict.items()]

_cached_skins = None

def get_skins():
    """
    Returns available skins based on richtemplates.settings.SKINS dict.
    """
    global _cached_skins
    if _cached_skins is None:
        _cached_skins = get_skins_from_dict(richtemplates.settings.SKINS)
    return _cached_skins

def get_skin_by_alias(alias):
    """
    Returns ``RichSkin`` object with given ``alias`` from available
    skins or raises SkinDoesNotExist exception.
    """
    skins = get_skins()
    for skin in skins:
        if skin.alias == alias:
            return skin
    raise SkinDoesNotExist("Skin with alias '%s' is not available. Check "
        "your settings file (available skins are: %s)"
        % (alias,  pformat([skin.alias for skin in skins])))

def get_skin_from_request(request):
    """
    Returns ``RichSkin`` object for the given request.
    If request's user is AnonymousUser skin would be taken from session.
    If there is no skin information in the session (key name is defined
    by ``RICHTEMPLATES_SESSION_SKIN_NAME`` setting) default skin would be
    returned. Same if authenticated user's profile has no information on
    skin (or profile is not available at all).
    If possible, skin would be taken form user's profile.
    """
    user = getattr(request, 'user', None)
    profile_model = get_user_profile_model()
    # Check if profile model is specified and user authed
    if profile_model and user.is_authenticated():
        try:
            profile = user.get_profile()
            alias = getattr(profile, richtemplates.settings.PROFILE_SKIN_FIELD,
                None)
            if alias:
                skin = get_skin_by_alias(alias)
                return skin
        except profile_model.DoesNotExist:
            logging.debug("Profile specified but not available for user %s. "
                "Will fallback to ``get_skin_from_session`` method." % user)
    skin = get_skin_from_session(request.session)
    return skin

def get_skin_from_session(session):
    """
    Returns ``RichSkin`` object from the session instance (from key
    ``RICHTEMPLATES_SESSION_SKIN_NAME``) or default skin if session
    does not provide skin information. Default skin is specified
    with ``RICHTEMPLATES_DEFAULT_SKIN`` setting.
    """
    session_skin_name = richtemplates.settings.SESSION_SKIN_NAME
    if session_skin_name in session:
        alias = session[session_skin_name]
    else:
        alias = richtemplates.settings.DEFAULT_SKIN
    skin = get_skin_by_alias(alias)
    return skin

def set_skin_at_request(request, skin_alias):
    """
    Sets skin on the given ``request`` instance.
    If user from request is authenticated and has profile with skin field
    (defined at ``RICHTEMPLATES_PROFILE_SKIN_FIELD``) then skin is set
    there. Otherwise, skin is set on the session.
    """
    if skin_alias not in richtemplates.settings.SKINS.keys():
        raise SkinDoesNotExist("Skin '%s' is not available")
    user = getattr(request, 'user', None)
    profile_model = get_user_profile_model()
    if profile_model and user.is_authenticated():
        try:
            profile = user.get_profile()
            profile.skin = skin_alias
            profile.save()
            logging.debug("Set skin %s for user %s in his/her profile"
                % (skin_alias, user))
            # Do not store skin on session if profile is available
            # as at the time user logs out his/her session is destroyed
            return
        except profile_model.DoesNotExist:
            pass
    set_skin_at_session(request.session, skin_alias)

def set_skin_at_session(session, skin_alias):
    """
    Sets skin info at given ``session`` object.
    """
    if skin_alias not in richtemplates.settings.SKINS.keys():
        raise SkinDoesNotExist("Skin '%s' is not available")
    session[richtemplates.settings.SESSION_SKIN_NAME] = skin_alias

