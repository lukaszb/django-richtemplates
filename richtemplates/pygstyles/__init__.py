

def get_all_styles():
    """
    Returns previously registered by richtemplates at
    ``richtemplates.settings.REGISTERED_PYGMENTS_STYLES``.
    """
    from richtemplates.settings import REGISTERED_PYGMENTS_STYLES
    return REGISTERED_PYGMENTS_STYLES

def get_style(alias):
    """
    Returns pygments style class. Available styles may be retrieved using
    ``get_all_styles`` method.
    """
    return get_all_styles()[alias]

