from django.conf.urls import patterns, include, url
from django.contrib import admin
from letter.urls import *

urlpatterns = patterns('',
    url(r'^', include('letter.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
