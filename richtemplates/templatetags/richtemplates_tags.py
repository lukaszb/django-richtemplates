from django import template
from django.template.defaultfilters import stringfilter, force_escape
from django.utils.safestring import mark_safe

import richtemplates.settings
from richtemplates.skins import get_skins
from richtemplates.skins import get_skin_by_alias
from richtemplates.skins import get_skin_from_request

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
        if len(value)  > max_length:
            output += '...'
    else:
        output = value
    value = force_escape(value)
    output = force_escape(output)
    output = '<span class="show-tipsy" title="%s">%s</span>' % (value, output)
    return mark_safe(output)

@register.tag(name='get_richskin')
def do_get_richskin(parser, token):
    """
    Parses tag that's supposed to be in this format:
    {% get_richskin ["skin_alias"] %}.
    ``skin_alias`` string is optional and if given tag would return skin object
    with same ``alias`` value.
    By default, ``skin`` context variable would be set.
    """
    bits = [b for b in token.split_contents()]
    format = '{% get_richskin ["skin_alias"] %}'
    if len(bits) == 1:
        tag_name, skin_alias = bits[0], None
    elif len(bits) == 2:
        tag_name, skin_alias = bits
        if not (skin_alias[0] == skin_alias[-1]
                and skin_alias[0] in ('"', "'")):
            raise template.TemplateSyntaxError, "%r tag's argument should be "\
                "in quotes" % tag_name
        else:
            skin_alias = skin_alias[1:-1]
            if not skin_alias in richtemplates.settings.SKINS.keys():
                raise template.TemplateSyntaxError, "%r is not proper "\
                    "skin alias (does not exist)" % skin_alias
    else:
        raise template.TemplateSyntaxError, "%r should be in format: "\
            '%s' % (tag_name, format)

    return RichSkinNode(skin_alias)

class RichSkinNode(template.Node):
    """
    Renders ``richskin`` tag. In fact, this is a shortcut to get ``link``
    tag used to pull stylesheet. If ``skin_alias`` is specified, link to
    this skin would be returned. Otherwise, tag would check the context's
    request (user and session).
    """
    def __init__(self, skin_alias, context_var='skin'):
        self.skin_alias = skin_alias
        self.context_var = context_var

    def render(self, context):
        if self.skin_alias is not None:
            skin = get_skin_by_alias(self.skin_alias)
        else:
            request = context['request']
            skin = get_skin_from_request(request)
        context[self.context_var] = skin
        return ''

class RichSkinListNode(template.Node):
    def __init__(self, context_var):
        self.context_var = context_var

    def render(self, context):
        skins = get_skins()
        context[self.context_var] = skins
        return ''

@register.tag
def get_skin_list(parser, token):
    """
    Parses ``get_skin_list`` tag which should be in format:
    {% get_skin_list [as context_var] %}
    By default, ``skin_list`` context variable would be set.
    """
    bits = token.split_contents()
    if len(bits) not in (1, 3):
        raise template.TemplateSyntaxError("get_skin_list tag should be in "
            "format: {% get_skin_list [as context_var] %}")
    context_var = 'skin_list'
    if len(bits) == 3:
        if bits[1] != 'as':
            raise template.TemplateSyntaxError("get_skin_list tag should be "
                "in format: {% get_skin_list [as context_var] %}")
        context_var = bits[2]
    return RichSkinListNode(context_var)

