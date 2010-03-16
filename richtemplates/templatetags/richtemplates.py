from django import template
from django.template.defaultfilters import stringfilter, force_escape, slice_
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
@stringfilter
def tooltip(value, max_length=None):
    """
    Adds tooltip mechanism to the given value by
    embracing it with 'span' tag with proper class.
    If `max_length` parameter is given, value
    would be chopped down to the given length and 
    three dots would be added.
    See ``common.js`` file (located within media
    directory) for details how tooltips are created
    with javascript.
    """
    if max_length:
        max_length = int(max_length)
        output = value[:max_length]
        if len(value) - 3 > max_length:
            output += '...'
    else:
        output = value
    value = force_escape(value)
    output = force_escape(output)
    output = '<span class="show-tooltip" title="%s">%s</span>' % (value, output)
    return mark_safe(output)

