from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'serofero.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^index/', views.index, name='index'),
                       url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
                       url(r'^page/(?P<pk>[\w\-]+)/$', views.page, name='page')
                       )
