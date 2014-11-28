__author__ = 'Gemini'
# coding=utf-8
from django.conf.urls import patterns, include, url
from mainapp.mviews import *

urlpatterns = patterns(
    '',
    url(r'^login$', login_view),
    url(r'^info$', get_info),
    url(r'^$', login_view),
)


