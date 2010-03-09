from django.conf import settings
from richtemplates.utils import register_rst_directives

RESTRUCTUREDTEXT_DIRECTIVES = getattr(settings,
    'RICHTEMPLATES_RESTRUCTUREDTEXT_DIRECTIVES', {})

register_rst_directives(RESTRUCTUREDTEXT_DIRECTIVES.items())

