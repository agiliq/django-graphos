from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'plot_model_data/(?P<model_name>\w+)/(?P<field_name>\w+)/(?P<count>\d+)/', \
                                'graphos.views.plot_model_data', name='plot_model_data'),
)

