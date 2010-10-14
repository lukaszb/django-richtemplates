from django.contrib.markup.templatetags.markup import restructuredtext
from django.http import HttpResponse, Http404
from django.views.generic.simple import direct_to_template
from django.utils.safestring import mark_safe
from django.utils.simplejson import dumps

from docutils.utils import SystemMessage

from richtemplates.settings import RESTRUCTUREDTEXT_PARSER_MAX_CHARS


def handle403(request, template_name='403.html'):
    """
    Default error 403 (Permission denied) handler.
    """
    response = direct_to_template(request, template=template_name)
    response.status_code = 403
    return response


def rst_preview(request):
    """
    Returns rendered restructured text.
    """
    def get_rst_error_as_html(message, title='Parser error occured'):
        """
        Returns restructured text error message as html. Manual marking as safe
        is required for rendering.
        """
        html = '\n'.join((
            '<div class="system-message">',
            '<p class="system-message-title">%s</p>' % title,
            message,
            '</div>',
        ))
        return html

    if not request.is_ajax() or not request.method == 'POST':
        raise Http404()
    data = request.POST.get('data', '')
    if len(data) > RESTRUCTUREDTEXT_PARSER_MAX_CHARS:
        html = get_rst_error_as_html('Text is too long (%s). Maximum is %s.' %
            (len(data), RESTRUCTUREDTEXT_PARSER_MAX_CHARS))
    else:
        try:
            html = restructuredtext(data)
        except SystemMessage:
            html = get_rst_error_as_html(
                'Sorry but there are at severe errors in your text '
                'and we cannot show it\'s preview.')
    rendered = mark_safe(html)
    return HttpResponse(dumps(rendered), mimetype='application/json')

