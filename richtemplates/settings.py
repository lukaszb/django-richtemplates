import logging

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.template.defaultfilters import slugify
from docutils.parsers.rst import directives

NOT_RENDER_SKINS = ('aqua',)
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
        raise ImproperlyConfigured("RICHTEMPLATES_SKINS needs to be a dict")
    SKINS.update(**skins)
    for skin, info in SKINS.items():
        if skin != slugify(skin):
            raise ImproperlyConfigured("Alias of the skin must be a slug")
        else:
            SKINS[skin]['alias'] = skin

        if 'url' not in info.keys():
            SKINS[skin]['url'] = settings.MEDIA_URL + 'richtemplates/css/' +\
                'skins/' + SKINS[skin]['alias'] + '.css'
        elif not info['url'].startswith('/'):
            SKINS[skin]['url'] = ''.join((settings.MEDIA_URL, info['url']))

        if 'name' not in info.keys():
            SKINS[skin]['name'] = skin


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

