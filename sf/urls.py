from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^index/', views.index, name='index'),
	url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
	url(r'^page/(?P<pk>[\w\-]+)/$', views.page, name='page'),
	)
