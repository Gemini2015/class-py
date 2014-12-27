from django.conf.urls import patterns, include, url
from mainapp.views import *
from django.conf import settings

urlpatterns = patterns('',
	url(r'^index$',main_view),
	url(r'^login$', login_view),
	url(r'^logout$', logout_view),
	url(r'^password$',password_view),
	url(r'^info/(?P<userid>\d+)$', info_view),
	url(r'^editinfo/(?P<userid>\d+)$',editinfo_view),
	url(r'^newuser$', newuser_view),
	url(r'^deleteuser$', deleteuser_view),
    url(r'^activity$', activity_main_view),
    url(r'^activity_new', activity_new_view),
	url(r'^$', login_view),
	)

# if settings.DEBUG is False:   #if DEBUG is True it will be served automatically
#     urlpatterns += patterns('',
#             url(r'^static/(?P.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
#     )
