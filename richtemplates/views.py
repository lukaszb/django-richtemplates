from django.contrib.markup.templatetags.markup import restructuredtext
from django.http import HttpResponse, Http404
from django.views.generic.simple import direct_to_template
from django.utils.simplejson import dumps

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
    if not request.is_ajax() or not request.method == 'POST':
        raise Http404()
    data = request.POST.get('data', '')
    rendered = restructuredtext(data)
    return HttpResponse(dumps(rendered), mimetype='application/json')

