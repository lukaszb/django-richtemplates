"""
Richtemplates is a set of templates (surprise!), template tags, media files
providing presentation layer for Django based projects, similar to what
Richfaces library offers for J2EE developers - not outstanding but still nice
looking and elegant.
"""

VERSION = (0, 3, 13, 'dev')

__version__ = '.'.join((str(each) for each in VERSION[:4]))

def get_version():
    """
    Returns shorter version (digit parts only) as string.
    """
    return '.'.join((str(each) for each in VERSION[:3]))

