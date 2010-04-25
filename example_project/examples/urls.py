from django.conf.urls.defaults import *

urlpatterns = patterns('django.views.generic.simple',
    url(r'^$',
        view='redirect_to',
        kwargs={'url': 'home'},
        name='richtemplates_examples'),

    url(r'^home/$',
        view='direct_to_template',
        kwargs={'template': 'examples/home.html'},
        name='richtemplates_examples_home'),

    url(r'^messages/$',
        view='direct_to_template',
        kwargs={'template': 'examples/messages.html',
            'extra_context': {
                'tags': ['debug', 'info', 'success', 'warning', 'info']},
        },
        name='richtemplates_examples_messages'),

    url(r'^links/$',
        view='direct_to_template',
        kwargs={'template': 'examples/links.html'},
        name='richtemplates_examples_links'),

    url(r'tooltips/$',
        view='direct_to_template',
        kwargs={'template': 'examples/tooltips.html'},
        name='richtemplates_examples_tooltips'),

)

urlpatterns += patterns('examples.views',
    url(r'^colors/$', 'colors', name='richtemplates_examples_colors'),
    url(r'^forms/form1/$', 'form1', name='richtemplates_examples_form1'),
    url(r'^forbidden/$', 'forbidden', name='richtemplates_examples_forbidden'),
    url(r'^set_skin/(?P<skin>[-\w]+)/$', 'set_skin', name='richtemplates_examples_set_skin'),
    url(r'^manage-user-groups/(?P<username>\w+)/$',
        view='manage_user_groups',
        name='richtemplates_examples_manage_user_groups'),

    url(r'^projects/$',
        view='project_list',
        name='richtemplates_examples_project_list'),
    url(r'^projects/(?P<project_id>\d+)/$',
        view='project_detail',
        name='richtemplates_examples_project_detail'),
    url(r'^projects/(?P<project_id>\d+)/tasks/$',
        view='project_task_list',
        name='richtemplates_examples_project_task_list'),
    url(r'^tasks/$',
        view='task_list',
        name='richtemplates_examples_task_list'),
    url(r'^tasks/(?P<task_id>\d+)/$',
        view='task_detail',
        name='richtemplates_examples_task_detail'),
    url(r'^tasks/(?P<task_id>\d+)/edit/$',
        view='task_edit',
        name='richtemplates_examples_task_edit'),
)

urlpatterns += patterns('',
    url(r'^richtemplates/', include('richtemplates.urls')),
)
