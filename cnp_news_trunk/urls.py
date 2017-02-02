from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from letter.urls import *
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^account/', include('django_authopenid.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('letter.urls'))
)

if settings.DEBUG:
    urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'', include('django.contrib.staticfiles.urls')),
) + urlpatterns