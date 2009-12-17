from django import template

import logging


def do_pygmentize(parser, token):
    logging.info("doing do_pygment_code:\n\tparser: %s\n\ttoken: %s\n"
        % (parser, token))
    try:
        tag_name, code, _options = token.split_contents()
    except ValueError:
        try:
            tag_name, code = token.split_contents()
            _options = "''" # Defaults to empty string
        except ValueError:
            raise template.TemplateSyntaxError, "%r tag requires at least " \
                "code argument." % token.contents.split()[0]
    if not (_options[0] == _options[-1] and _options[0] in ['"', "'"]):
        raise template.TemplateSyntaxError, "%r tag's options should be " \
            " in quotes" % tag_name
    options = dict(((opt, True) for opt in _options[1:-1].split(',')))
    options.setdefault('lineno', True)
    options.setdefault('lineanchors', False)
    
    return PygmentizeNode(code, options)

