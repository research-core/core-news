from django.conf.urls import patterns, include, url
from views import user_profile

urlpatterns = patterns('',
	url(r'^accounts/profile/$', user_profile, name='user_profile'),
)
 