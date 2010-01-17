from django.conf.urls.defaults import *

urlpatterns = patterns('django.views.generic.simple',
    url(r'^$', 
        view='redirect_to',
        kwargs={'url': 'home'},
        name='richtemplates_examples'),

    url(r'^home/$',
        view='direct_to_template',
        kwargs={'template': 'richtemplates/examples/home.html'},
        name='richtemplates_examples_home'),

    url(r'^messages/$',
        view='direct_to_template',
        kwargs={'template': 'richtemplates/examples/messages.html',
            'extra_context': {
                'tags': ['debug', 'info', 'success', 'warning', 'info']},
        },
        name='richtemplates_examples_messages'),

    url(r'^links/$',
        view='direct_to_template',
        kwargs={'template': 'richtemplates/examples/links.html'},
        name='richtemplates_examples_links'),

)

urlpatterns += patterns('richtemplates.examples.views',
    url(r'^colors/$', 'colors', name='richtemplates_examples_colors'),
    url(r'^forms/form1/$', 'form1', name='richtemplates_examples_form1'),
)

