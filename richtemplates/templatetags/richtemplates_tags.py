import logging

from django import template
from django.template.defaultfilters import stringfilter, force_escape, slice_
from django.utils.safestring import mark_safe

from richtemplates import settings as richtemplates_settings
from richtemplates.utils import get_skin_for_request

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


def do_richskin(parser, token):
    """
    Parses tag that's supposed to be in this format:
    {% richskin ["skin_alias"] %}. ``skin_alias`` string is optional.
    """
    bits = [b for b in token.split_contents()]
    if len(bits) == 1:
        tag_name, skin_alias = bits[0], None
        logging.info("Tag name: %s | Skin alias: %s" % (tag_name, skin_alias))
    elif len(bits) == 2:
        tag_name, skin_alias = bits
        if not (skin_alias[0] == skin_alias[-1]
                and skin_alias[0] in ('"', "'")):
            raise template.TemplateSyntaxError, "%r tag's argument should be "\
                "in quotes" % tag_name
        else:
            skin_alias = skin_alias[1:-1]
            if not skin_alias in richtemplates_settings.SKINS.keys():
                raise template.TemplateSyntaxError, "%r is not proper "\
                    "skin alias (does not exist)" % skin_alias
    else:
        raise template.TemplateSyntaxError, "%r should be in format: "\
            '{% %r ["skin_alias"] %}' % (tag_name, tag_name)
    
    logging.info("Returning RichSkinNode with skin_alias: %s" % skin_alias)
    return RichSkinNode(skin_alias)

class RichSkinNode(template.Node):
    """
    Renders ``richskin`` tag. In fact, this is a shortcut to get ``link``
    tag used to pull stylesheet. If ``skin_alias`` is specified, link to
    this skin would be returned. Otherwise, tag would check the context's
    request (user and session).
    """
    def __init__(self, skin_alias):
        self.skin_alias = skin_alias
    def render(self, context):
        link_tag = u'<link rel="stylesheet" type="text/css" href="%s" />'
        if self.skin_alias is not None:
            skin = richtemplates_settings.SKINS[self.skin_alias]
        else:
            request = context['request']
            skin = get_skin_for_request(request)
            logging.info("From get_skin_for_request got %s" % skin)
            if skin['alias'] in richtemplates_settings.NOT_RENDER_SKINS:
                return '' 

            if not richtemplates_settings.SESSION_SKIN_NAME in request.session:
                request.session[richtemplates_settings.SESSION_SKIN_NAME] = skin['alias']
            logging.info("Skin in session: %s" % request.session[richtemplates_settings.SESSION_SKIN_NAME])
            if skin['alias'] != request.session[richtemplates_settings.SESSION_SKIN_NAME]:
                logging.info("Skin is not same as one in session")
                if hasattr(request, 'user') and request.user.is_authenticated():
                    profile = request.user.get_profile()
                    setattr(profile, richtemplates_settings.PROFILE_SKIN_FIELD,
                        skin['alias'])
            if not 'url' in skin:
                logging.info("returned skin has no url")
            logging.debug("Skin's url: %s" % skin['url'])
        result = link_tag % skin['url']
        logging.info("RichSkinNode renders:\n%s" % result)
        return result

register.tag('richskin', do_richskin)

