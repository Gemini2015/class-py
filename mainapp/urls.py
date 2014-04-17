from django.conf.urls import patterns, include, url
from mainapp.views import *

urlpatterns = patterns('',
	url(r'^index$',main_view),
	url(r'^login$', login_view),
	url(r'^logout$', logout_view),
	url(r'^password$',password_view),
	url(r'^info/(?P<userId>\d+)$', info_view),
	url(r'^editinfo/(?P<userId>\d+)$',editinfo_view),
	url(r'^newuser$', newuser_view),
	url(r'^deleteuser$', deleteuser_view),
	url(r'^$', login_view),
	)