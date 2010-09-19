from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.simplejson import dumps


def bars(request, template_name='examples/jqplot/bars.html'):

    context = {}

    data = [
        ['2008-09-30', 4],
		['2008-10-30', 6.5],
		['2008-11-30', 5.7],
		['2008-12-30', 9],
		['2009-01-30', 8.2],
    ]
    data2 = [ [data[i][0], data[-i][1]] for i in xrange(len(data)) ]

    context['data'] = dumps(data)
    context['data2'] = dumps(data2)

    return render_to_response(template_name, context, RequestContext(request))
