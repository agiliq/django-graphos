from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', 'demo.views.home', name='demo_home'),
    url(r'^tutorial/$', 'demo.views.tutorial', name='demo_tutorial'),
    url(r'^gchart/$', 'demo.views.gchart_demo', name='demo_gchart_demo'),
    url(r'^yui/$', 'demo.views.yui_demo', name='demo_yui_demo'),
    url(r'^flot/$', 'demo.views.flot_demo', name='demo_flot_demo'),
    url(r'^morris/$', 'demo.views.morris_demo', name='demo_morris_demo'),
    url(r'^time_series/$', 'demo.views.time_series_demo',
                           name='demo_time_series_example'),
)
