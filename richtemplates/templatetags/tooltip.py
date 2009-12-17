from django import template
from django.template.defaultfilters import stringfilter, force_escape, slice_
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
@stringfilter
def tooltipped(value, max_length=None):
    """
    Adds tooltip mechanism to the given value by
    embracing it with 'span' tag with proper class.
    If `max_length` parameter is given, value
    would be chopped down to the given length and 
    three dots would be added.
    """
    if max_length:
        max_length = int(max_length)
        output = value[:max_length]
    output = force_escape(output)
    output = '<span class="show-tooltip">' + output + '</span>'
    return mark_safe(output)


