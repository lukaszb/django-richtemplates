"""
In order to use those directives add RICHTEMPLATES_RESTRUCTUREDTEXT_DIRECTIVES
dictionary in your settings module.

For example, put following dict in settings.py:

RICHTEMPLATES_RESTRUCTUREDTEXT_DIRECTIVES = {
    'code-block': 'richtemlates.rstdirectives.pygments_directive',
}

"""
from docutils import nodes
from docutils.parsers.rst import Directive, directives

from django.core.exceptions import ImproperlyConfigured

try:
    from pygments import highlight
    from pygments.formatters import HtmlFormatter
    from pygments.lexers import get_lexer_by_name, TextLexer
except ImportError:
    raise ImproperlyConfigured("Install pygments first")

class CodeBlock(Directive):
    """
    Directive for a code block with pygments support.  Took from Sphinx,
    excellent documentation generator http://sphinx.pocoo.org/
    """

    has_content = True
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        'linenos': directives.flag,
    }

    def run(self):
        try:
            lexer = get_lexer_by_name(self.arguments[0])
        except ValueError:
            # default lexer
            lexer = TextLexer()
        linenos = 'linenos' in self.options
        formatter = HtmlFormatter(linenos=linenos, cssclass="code-highlight",
            lineanchors='line', anchorlinenos=True)
        parsed = highlight(u'\n'.join(self.content), lexer, formatter)
        parsed = '<div class="codeblock">%s</div>' % parsed
        return [nodes.raw('', parsed, format='html')]

