"""
In order to use those directives add RICHTEMPLATES_RESTRUCTUREDTEXT_DIRECTIVES
dictionary in your settings module.

For example, put following dict in settings.py:

RICHTEMPLATES_RESTRUCTUREDTEXT_DIRECTIVES = {
    'code-block': 'richtemlates.rstdirectives.pygments_directive',
}

"""
from docutils import nodes
from django.core.exceptions import ImproperlyConfigured

try:
    from pygments import highlight
    from pygments.formatters import HtmlFormatter
    from pygments.lexers import get_lexer_by_name, TextLexer
except ImportError:
    raise ImproperlyConfigured("Install pygments first")

def pygments_directive(name, arguments, options, content, lineno,
        content_offset, block_text, state, state_machine):
    try:
        lexer = get_lexer_by_name(arguments[0])
    except ValueError:
        # default lexer
        lexer = TextLexer()
    formatter = HtmlFormatter(linenos=True, cssclass="code-highlight",
        lineanchors='line', anchorlinenos=True)
    parsed = highlight(u'\n'.join(content), lexer, formatter)
    parsed = '<div class="codeblock">%s</div>' % parsed
    return [nodes.raw('', parsed, format='html')]

pygments_directive.arguments = (1, 0, 1)
pygments_directive.content = 1

