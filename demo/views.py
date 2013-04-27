import urllib2
import logging
import json
from random import randrange

from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from django.core.cache import cache
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect, HttpResponseNotModified, \
                        HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import TimeSeries

from graphos.renderers.flot import LineChart

@csrf_exempt
def home(request):
    """
    Try a POST with curl and automatically adds a random value, this updates plot async
    """
    if request.POST and 'model_data' in request.POST.values():
        try:
            last_value = TimeSeries.objects.order_by('-id')[0].value
        except:
            last_value = 50
        if last_value < 5 or last_value > 100:
            last_value = 50
        TimeSeries.objects.create(value=randrange(last_value - 5, last_value + 5))

    if request.POST and 'redis_data' in request.POST.values():
        try:
            import redis
        except ImportError, e:
            logging.error("redis -redis server binding for Python is not installed. \
                                            Try pip install redis")
        try:
            from redis import ConnectionError
            r_inst = redis.Redis('localhost')  # works only on local
            r_inst.ping()
        except ConnectionError:
            logging.error("redis server is not running. Start it to make graphos plot data.")
        #        import redis
        #        r_inst = redis.Redis('localhost')
        r_inst.rpush('graphos', randrange(1, 100))

    series = [
                ['Year', 'Sales', 'Expenses'],
                ['2004',  1000,      400],
                ['2005',  1170,      460],
                ['2006',  660,       1120],
                ['2007',  1030,      540]
            ]

    Chart = LineChart(series)

    c = RequestContext(request)
    return render_to_response('home.html', {'Chart': TimeSeriesChart}, context_instance=c)

def tutorial(request):
    """
    Try a POST with curl and automatically adds a random value, this updates plot async
    """
    if request.POST and 'model_data' in request.POST.values():
        try:
            last_value = TimeSeries.objects.order_by('-id')[0].value
        except:
            last_value = 50
        if last_value < 5 or last_value > 100:
            last_value = 50
        TimeSeries.objects.create(value=randrange(last_value - 5, last_value + 5))

    if request.POST and 'redis_data' in request.POST.values():
        try:
            import redis
        except ImportError, e:
            logging.error("redis -redis server binding for Python is not installed. \
                                            Try pip install redis")
        try:
            from redis import ConnectionError
            r_inst = redis.Redis('localhost')  # works only on local
            r_inst.ping()
        except ConnectionError:
            logging.error("redis server is not running. Start it to make graphos plot data.")
        #        import redis
        #        r_inst = redis.Redis('localhost')
        r_inst.rpush('graphos', randrange(1, 100))

    c = RequestContext(request, {

    })
    return render_to_response('tutorial.html', context_instance=c)

