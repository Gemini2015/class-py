# coding=utf-8
from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Classmates.views.home', name='home'),
    # url(r'^Classmates/', include('Classmates.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^', include('mainapp.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^m/', include('mainapp.murls')),

)


# 当 Debug 设置为 False，Django不能自动处理静态文件
if settings.DEBUG is False:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.STATIC_ROOT,
        }),
   )