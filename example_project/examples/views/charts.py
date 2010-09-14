import pyofc2
import urllib2

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.simplejson import loads

def chart(request, chart_data_url, title='chart',
        template_name='examples/chart.html'):
    return render_to_response(template_name, {
        'chart_data_url': chart_data_url,
        'title': title},
        RequestContext(request))

def bars(request):
    return chart(request,
        chart_data_url=reverse('richtemplates_examples_charts_bars_data'),
        title='Bars chart')

def bars_data(request):
    url = 'https://api.bitbucket.org/1.0/repositories/lukaszb/django-richtemplates/changesets/'
    response = urllib2.urlopen(url)
    jdata = loads(response.read())
    changesets = jdata['changesets']

    added = pyofc2.bar()
    modified = pyofc2.bar()
    removed = pyofc2.bar()
    added.values, modified.values, removed.values = [], [], []
    added.colour = '#00c700'
    added.text = 'Added'
    modified.colour = '#ffaa00'
    modified.text = 'Modified'
    removed.colour = '#f27474'
    removed.text = 'Removed'

    x = pyofc2.x_axis()
    y = pyofc2.y_axis(steps=5)
    y_max = 0
    labels = []

    for changeset in changesets:
        labels.append(pyofc2.x_axis_label(text='%s:%s' %
            (changeset['revision'], changeset['node'])))
        files = changeset['files']
        tip = '#val#<br>Date: %s<br>Revision: %s:%s<br>Author: %s<br>Message: %s'
        tip = tip % tuple([changeset[key] for key in (
            'timestamp', 'revision', 'node', 'author', 'message')])
        tip = '%s: ' + tip
        # Added files
        added_count = len([f for f in files if f['type'] == 'added'])
        added.values.append(pyofc2.barvalue(top=added_count, tip=tip % 'Added'))
        # Modified files
        modified_count = len([f for f in files if f['type'] == 'modified'])
        modified.values.append(pyofc2.barvalue(top=modified_count,
            tip=tip % 'Modified'))
        # Removed files
        removed_count = len([f for f in files if f['type'] == 'removed'])
        removed.values.append(pyofc2.barvalue(top=removed_count,
            tip=tip % 'Removed'))
        y_max = max([y_max, added_count, modified_count, removed_count])

    y.min = 0
    y.max = y_max

    title = pyofc2.title(text='django-richtemplates changesets')
    chart = pyofc2.open_flash_chart()
    chart.title = title
    chart.add_element(added)
    chart.add_element(modified)
    chart.add_element(removed)
    chart.bg_colour = '#ffffff'
    x.labels = pyofc2.x_axis_labels(steps=1, rotate=25.0)
    x.labels.labels = labels
    chart.x_axis = x
    chart.y_axis = y
    return HttpResponse(chart.render(), mimetype='application/json')

