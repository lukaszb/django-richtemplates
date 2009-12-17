from django.conf.urls.defaults import *

urlpatterns = patterns('django.views.generic.simple',
    url(r'^$', 'redirect_to', {'url': 'home'}, name='richtemplates_examples'),
    url(r'^home/$', 'direct_to_template', {'template':
        'richtemplates/examples/home.html'},
        name='richtemplates_examples_home'),
    url(r'^messages/$', 'direct_to_template',
        {'template': 'richtemplates/examples/messages.html',
            'extra_context': {
                'tags': ['debug', 'info', 'success', 'warning', 'info']},
        },
        name='richtemplates_examples_messages'),
    url(r'^links/$', 'direct_to_template',
        {'template': 'richtemplates/examples/links.html'},
        name='richtemplates_examples_links'),

)

urlpatterns += patterns('richtemplates.examples.views',
    url(r'^colors/$', 'colors', name='richtemplates_examples_colors'),
)

