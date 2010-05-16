from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

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

if settings.RICHTEMPLATES_USE_DAJAX:
    urlpatterns += patterns('',
        (r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),
    )

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^%s/(?P<path>.*)$' % settings.MEDIA_URL.strip('/'),
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
)

