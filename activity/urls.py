__author__ = 'chengche'
from django.conf.urls import patterns, include, url
from activity.views import *
from django.conf import settings

urlpatterns = patterns('',
                       url(r'^new', activity_new_view),
                       url(r'^(?P<activity_id>\d+)$', activity_info_view),
                       url(r'^join$', activity_join_view),
                       url(r'^quit$', activity_quit_view),
                       url(r'^post_comment$', activity_post_comment_view),
                       url(r'^del_comment$', activity_del_comment_view),
                       url(r'^change_status$', activity_change_status_view),
                       url(r'^del_activity$', activity_del_activity_view),
                       url(r'^$', activity_main_view),
                       )

# if settings.DEBUG is False:   #if DEBUG is True it will be served automatically
# urlpatterns += patterns('',
# url(r'^static/(?P.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
# )
