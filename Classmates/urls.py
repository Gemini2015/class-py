from django.conf.urls import patterns, include, url

from django.contrib import admin

#from mainapp.views import login

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Classmates.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('mainapp.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
)
