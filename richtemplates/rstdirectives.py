from docutils import nodes

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, TextLexer

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

