from django.conf.urls import patterns, include, url
from django.contrib import admin
from sf import urls as sfurls

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'serofero.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(sfurls)),
)
