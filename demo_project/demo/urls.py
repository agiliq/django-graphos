from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', 'demo.views.home', name='demo_home'),
    url(r'^tutorial/$', 'demo.views.tutorial', name='demo_tutorial'),
    url(r'^gchart/$', 'demo.views.gchart_demo', name='demo_gchart_demo'),
    url(r'^yui/$', 'demo.views.yui_demo', name='demo_yui_demo'),
    url(r'^flot/$', 'demo.views.flot_demo', name='demo_flot_demo'),
    url(r'^highcharts/$', 'demo.views.highcharts_demo', name='demo_highcharts_demo'),
    url(r'^c3js/$', 'demo.views.c3js_demo', name='demo_c3js_demo'),
    url(r'^morris/$', 'demo.views.morris_demo', name='demo_morris_demo'),
    url(r'^matplotlib/$', 'demo.views.matplotlib_demo', name='demo_matplotlib_demo'),
    url(r'^time_series/$', 'demo.views.time_series_demo',
                           name='demo_time_series_example'),
    url(r"^gchart-json/$", "demo.views.custom_gchart_renderer", name="demo_custom_gchart"),
    url(r"^mongo-json/$", "demo.views.mongo_json", name="demo_mongo_json"),
    url(r"^mongo-json2/$", "demo.views.mongo_json2", name="demo_mongo_json2"),
    url(r"^mongo-json-multi/$", "demo.views.mongo_json_multi", name="demo_mongo_json_multi"),
    url(r"^mongo-json-multi2/$", "demo.views.mongo_json_multi2", name="demo_mongo_json_multi2"),
)

