from djalog import DjalogLogger as logger

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
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
IMAGES_URL = MEDIA_URL + 'img/'
ICONS_URL = IMAGES_URL + 'icons/'

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

USE_DAJAX = getattr(settings, 'RICHTEMPLATES_USE_DAJAX', False)

DEFAULT_CODE_STYLE = getattr(settings,
    'RICHTEMPLATES_DEFAULT_CODE_STYLE', 'native')
PROFILE_CODE_STYLE_FIELD = getattr(settings,
    'RICHTEMPLATES_PROFILE_CODE_STYLE_FIELD', 'code_style')

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
            logger.debug(msg)
        except ImportError, err:
            msg = "Couldn't register restructuredText directive. Original "\
                "exception was: %s" % err
            logger.warn(msg)


RESTRUCTUREDTEXT_DIRECTIVES = getattr(settings,
    'RICHTEMPLATES_RESTRUCTUREDTEXT_DIRECTIVES', {})

register_rst_directives(RESTRUCTUREDTEXT_DIRECTIVES.items())


# ======================= #
# Pygments styles helpers #
# ======================= #

def register_pygments_style(pygment_styles):
    """
    Registers Pygments style classes. Pygments currently has plugin support at
    pkg_resources level whitch is not always straightforword. This method allows
    to register pygments styles easier and on the fly.

    Expects a dict with alias keys and classes/paths to classes values. Default
    pygments styles are always registered and you cannot override them (would
    raise ImproperlyConfigured exception). After style is registered, it may be
    received with ``richtemplates.pygstyles.get_style`` method which expects
    alias parameter.
    """
    try:
        from pygments.styles import STYLE_MAP, get_style_by_name
        from pygments.style import Style
    except ImportError:
        raise ImproperlyConfigured("pygments are required to use richtemplates")
    registry = {}
    for alias, style_path in pygment_styles.items():
        if alias in STYLE_MAP:
            raise ImproperlyConfigured("Cannot override builtin %s pygments "
                "styles" % alias)
        if isinstance(style_path, Style):
            klass = style_path
        else:
            try:
                splitted = style_path.split('.')
                mod_path, class_name = '.'.join(splitted[:-1]), splitted[-1]
                mod = __import__(mod_path, (), (), [class_name], -1)
                klass = getattr(mod, class_name)
            except (ImportError, AttributeError), err:
                raise ImproperlyConfigured("Cannot register style %s: %s.\n"
                    "Original error was: %s" % (alias, style_path, err))
        registry[alias] = klass
        logger.debug("Registered %s as pygments style with alias %s"
            % (klass.__name__, alias))
    for alias in STYLE_MAP:
        klass = get_style_by_name(alias)
        registry[alias] = klass
        logger.debug("Registered %s as pygments style with alias %s"
            % (klass.__name__, alias))
    return registry

PYGMENTS_STYLES = getattr(settings,
    'RICHTEMPLATES_PYGMENTS_STYLES', {})

REGISTERED_PYGMENTS_STYLES = register_pygments_style(PYGMENTS_STYLES)

