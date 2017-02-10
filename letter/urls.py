from django.conf.urls import url
from letter.views import show_newsletter, build_newsletter, build_event, test_newsletter, test_event, send_newsletter

urlpatterns = [
	url(r'^shownewsletter/(?P<scope>int)$',                                             show_newsletter  ),
	url(r'^shownewsletter/(?P<scope>int)/(?P<id>\d+)/$',                                show_newsletter  ),
	url(r'^shownewsletter/(?P<scope>int)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$',  show_newsletter  ),
	url(r'^shownewsletter/(?P<scope>int)/(?P<sdate>\d{4}\d{2}\d{2})/$',                 show_newsletter  ),

	url(r'^shownewsletter/(?P<scope>ext)$',                                             show_newsletter  ),
	url(r'^shownewsletter/(?P<scope>ext)/(?P<id>\d+)/$',                                show_newsletter  ),
	url(r'^shownewsletter/(?P<scope>ext)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$',  show_newsletter  ),
	url(r'^shownewsletter/(?P<scope>ext)/(?P<sdate>\d{4}\d{2}\d{2})/$',                 show_newsletter  ),

	url(r'^buildnewsletter/$',                                                          build_newsletter ),
	url(r'^buildnewsletter/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$',                build_newsletter ),

	url(r'^buildevent/$',                                                               build_event      ),
	url(r'^buildevent/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$',                     build_event      ),

	url(r'^testnewsletter/(?P<scope>int)$',                                             test_newsletter  ),
	url(r'^testnewsletter/(?P<scope>int)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$',  test_newsletter  ),

	url(r'^testnewsletter/(?P<scope>ext)$',                                             test_newsletter  ),
	url(r'^testnewsletter/(?P<scope>ext)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$',  test_newsletter  ),

	url(r'^testevent/$',                                                                test_event       ),
	url(r'^testevent/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$',                      test_event       ),

	url(r'^sendnewsletter/$',                                                           send_newsletter  ),
	url(r'^sendnewsletter/(?P<id>\d+)/$',                                               send_newsletter  ),
	url(r'^sendnewsletter/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$',                 send_newsletter  ),
]