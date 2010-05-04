"""
Overrides django-native-tags' contrib pygmentize module in order to
allow use of highlight_style tag with styles defined at richtemplates
settings.
"""
from native_tags.decorators import function, block

from richtemplates.settings import DEFAULT_CODE_STYLE
from richtemplates.pygstyles import get_style

from pygments import highlight as highlighter
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

def highlight_style(cssclass='highlight', **kwargs):
    """
    Returns the CSS from the ``HtmlFormatter``.
    ``cssclass`` is the name of the ``div`` css class to use

        Syntax::

            {% highlight_style [cssclass] [formatter options] %}

        Example::

            {% highlight_style code linenos=true %}

    .. note::
       This tag overrides default builtin django-native-tags in order to use
       richtemplates' pygments helpers (which allows to hook styles at settings
       module without having to play with pkg_resources).

    """
    alias = kwargs.pop('style', DEFAULT_CODE_STYLE)
    style = get_style(alias)
    kwargs['style'] = style
    return HtmlFormatter(**kwargs).get_style_defs('.%s' % cssclass)
highlight_style = function(highlight_style)

def highlight(code, lexer, **kwargs):
    """
    Returns highlighted code ``div`` tag from ``HtmlFormatter``
    Lexer is guessed by ``lexer`` name
    arguments are passed into the formatter

        Syntax::

            {% highlight [source code] [lexer name] [formatter options] %}

        Example::

            {% highlight 'print "Hello World"' python linenos=true %}
    """
    return highlighter(code or '', get_lexer_by_name(lexer), HtmlFormatter(**kwargs))
highlight = function(highlight, is_safe=True)

def highlight_block(context, nodelist, lexer, **kwargs):
    """
    Code is nodelist ``rendered`` in ``context``
    Returns highlighted code ``div`` tag from ``HtmlFormatter``
    Lexer is guessed by ``lexer`` name
    arguments are passed into the formatter

        Syntax::

            {% highlight_block [lexer name] [formatter options] %}
                ... source code ..
            {% endhighlight_block %}

        Example::

            {% highlight_block python linenos=true %}
                print '{{ request.path }}'
            {% endhighlight_block %}
    """
    return highlighter(nodelist.render(context) or '', get_lexer_by_name(lexer), HtmlFormatter(**kwargs))
highlight_block = block(highlight_block, is_safe=True)
