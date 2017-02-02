from django.conf.urls.defaults import *
#from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('letter.views',
    url(r'^admin/', include(admin.site.urls)),

    (r'^$', 'Home'),

    (r'^ShowNewsletter/(?P<scope>int)$', 'ShowNewsletter'),
    (r'^ShowNewsletter/(?P<scope>int)/(?P<id>\d+)/$', 'ShowNewsletter'),
    (r'^ShowNewsletter/(?P<scope>int)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', 'ShowNewsletter'),
    (r'^ShowNewsletter/(?P<scope>int)/(?P<sdate>\d{4}\d{2}\d{2})/$', 'ShowNewsletter'),

    (r'^ShowNewsletter/(?P<scope>ext)$', 'ShowNewsletter'),
    (r'^ShowNewsletter/(?P<scope>ext)/(?P<id>\d+)/$', 'ShowNewsletter'),
    (r'^ShowNewsletter/(?P<scope>ext)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', 'ShowNewsletter'),
    (r'^ShowNewsletter/(?P<scope>ext)/(?P<sdate>\d{4}\d{2}\d{2})/$', 'ShowNewsletter'),

    (r'^BuildNewsletter/$', 'BuildNewsletter'),
    (r'^BuildNewsletter/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', 'BuildNewsletter'),

    (r'^BuildEvent/$', 'BuildEvent'),
    (r'^BuildEvent/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', 'BuildEvent'),

    (r'^TestNewsletter/(?P<scope>int)$', 'TestNewsletter'),
    (r'^TestNewsletter/(?P<scope>int)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', 'TestNewsletter'),

    (r'^TestNewsletter/(?P<scope>ext)$', 'TestNewsletter'),
    (r'^TestNewsletter/(?P<scope>ext)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', 'TestNewsletter'),

    (r'^TestEvent/$', 'TestEvent'),
    (r'^TestEvent/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', 'TestEvent'),

    (r'^SendNewsletter/$', 'SendNewsletter'),
    (r'^SendNewsletter/(?P<id>\d+)/$', 'SendNewsletter'),
    (r'^SendNewsletter/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', 'SendNewsletter'),

)
