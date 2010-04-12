import logging

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.template.defaultfilters import slugify
from docutils.parsers.rst import directives

if 'django.core.context_processors.request' \
    not in settings.TEMPLATE_CONTEXT_PROCESSORS:
        raise ImproperlyConfigured("To use richtemplates you need to add "
            "'django.core.context_processors.request' to your "
            "TEMPLATE_CONTEXT_PROCESSORS")

if 'richtemplates.context_processors.media' \
    not in settings.TEMPLATE_CONTEXT_PROCESSORS:
        raise ImproperlyConfigured("To use richtemplates you need to add "
            "'richtemplates.context_processors.media' to your "
            "TEMPLATE_CONTEXT_PROCESSORS")

MEDIA_URL = getattr(settings, 'RICHTEMPLATES_MEDIA_URL',
    settings.MEDIA_URL + 'richtemplates/')

BASE_SKINS = ('aqua',)
SESSION_SKIN_NAME = getattr(settings, 'RICHTEMPLATES_SESSION_SKIN_NAME',
    'skin')
PROFILE_SKIN_FIELD = getattr(settings, 'RICHTEMPLATES_PROFILE_SKIN_FIELD',
    'skin')
DEFAULT_SKIN = getattr(settings, 'RICHTEMPLATES_DEFAULT_SKIN', 'aqua')
SKINS = {
    'aqua': {'name': 'Aqua'},
    'django': {'name': 'Django'},
    'ruby': {'name': 'Ruby'},
}

if hasattr(settings, 'RICHTEMPLATES_SKINS'):
    skins = getattr(settings, 'RICHTEMPLATES_SKINS')
    if not isinstance(skins, dict):
        raise ImproperlyConfigured("RICHTEMPLATES_SKINS needs to be a dict "
            "(is %s)" % type(skins))
    for alias, skin_info in skins.items():
        if not isinstance(alias, (str, unicode)):
            raise ImproperlyConfigured("Keys of RICHTEMPLATES_SKINS should "
                "be a string (is %s)" % type(alias))
        if not isinstance(skin_info, dict):
            raise ImproperlyConfigured("Values of RICHTEMPLATES_SKINS should "
                "be a dict (is %s)" % type(skin_info))
        allowed_keys = ('alias', 'name', 'url')
        if not set(skin_info.keys()).issubset(allowed_keys):
            raise ImproperlyConfigured("Wrong keys defined for skin '%s' "
                "(allowed keys: %s)" % (alias, allowed_keys))

    SKINS.update(**skins)

def register_rst_directives(directives_items):
    """
    Registers restructuredText directives given as dictionary
    with keys being names and paths to directive function.
    """
    for name, directive_path in directives_items:
        try:
            splitted = directive_path.split('.')
            mod_path, method_name = '.'.join(splitted[:-1]), splitted[-1]
            mod = __import__(mod_path, (), (), [method_name], -1)
            directive = getattr(mod, method_name)
            directives.register_directive(name, directive)
            msg = "Registered restructuredText directive: %s" % method_name
            logging.debug(msg)
        except ImportError, err:
            msg = "Couldn't register restructuredText directive. Original "\
                "exception was: %s" % err
            logging.warn(msg)


RESTRUCTUREDTEXT_DIRECTIVES = getattr(settings,
    'RICHTEMPLATES_RESTRUCTUREDTEXT_DIRECTIVES', {})

register_rst_directives(RESTRUCTUREDTEXT_DIRECTIVES.items())

