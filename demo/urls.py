from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'demo.views.home', name='demo_home'),
    url(r'^tutorial/$', 'demo.views.tutorial', name='demo_tutorial'),
    url(r'^gchart/$', 'demo.views.gchart_demo', name='demo_gchart_demo'),
    url(r'^yui/$', 'demo.views.yui_demo', name='demo_yui_demo'),
)
