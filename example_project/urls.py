from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.views.generic import TemplateView


admin.autodiscover()

urlpatterns = patterns('',
    (r'^accounts/', include('registration.urls')),
    url(r'^admin_tools/', include('admin_tools.urls')),
    (r'^admin/', include(admin.site.urls)),
    url(r'^users/(?P<username>\w+)/$',
        view='examples.views.userprofile',
        name='richtemplates_examples_userprofile'),
    url(r'^users/(?P<username>\w+)/edit/$',
        view='examples.views.userprofile_edit',
        name='richtemplates_examples_userprofile_edit'),


    # example app's urls
    (r'^', include('examples.urls')),
)

