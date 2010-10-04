from django.conf.urls.defaults import *

urlpatterns = patterns('richtemplates.views',
    url(r'rst_preview/$', view='rst_preview', name='richtemplates_rst_preview'),
)

