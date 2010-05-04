"""
These are native tags so in order to load them you need to::

    {% load native %}

in your templates.
"""
from richtemplates import settings as richtemplates_settings

def autocomplete_field(bfield, **opts):
    """
    Returns ``<script>`` tag with jquery-ui autocompletion for the given
    field. In order to get this working field have to specify ``queryset``
    attribute. You may pass options to autocomplete plugin and if you specify
    ``attr`` option, it would be used to represent available choices (default is
    ``__unicode__``).

    Syntax::

        {% autocomplete_field field [options] %}

    For example, lets say our form contains ``owner`` field which is a
    ``ModelChoiceField`` related with ``User`` model. If we pass form into
    the context, we can autocomplete it's ``owner`` field by putting following
    snippet somewhere in a template::

        {% autocomplete_field form.owner delay=0 %}

    """
    field_id = bfield.auto_id
    attr = opts.pop('attr', '__unicode__')
    assert hasattr(bfield.field.queryset.model, attr)
    choices = ( callable(item) and item() or item for item in
        (getattr(obj, attr) for obj in bfield.field.queryset))

    opts['source'] = '[' + ', '.join(('"%s"' % choice
        for choice in choices)) + ']'
    opts.setdefault('delay', 50)

    options = ', '.join(("%s: %s" % (key, val) for key, val in opts.items()))

    script_body = \
    """<script type="text/javascript">
        $(document).ready(function(){
            $('#%(field_id)s').autocomplete({%(options)s});
        });
    </script>
    """ % {'field_id': field_id, 'options': options}

    return script_body
autocomplete_field.function = True

def do_get_code_style(context):
    user = context['user']
    if user and user.is_authenticated():
        style = getattr(user.get_profile(),
            richtemplates_settings.PROFILE_CODE_STYLE_FIELD,
            richtemplates_settings.DEFAULT_CODE_STYLE)
    else:
        style = richtemplates_settings.DEFAULT_CODE_STYLE
    return style
do_get_code_style.function = True
do_get_code_style.takes_context = True
do_get_code_style.name = 'get_code_style'
