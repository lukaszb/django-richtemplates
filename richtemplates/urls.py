from django.conf.urls.defaults import *

urlpatterns = patterns('richtemplates.views',
    url(r'set_skin/(?P<skin>[-\w]+)/$', 'set_skin',
        name='richtemplates_set_skin'),
)

