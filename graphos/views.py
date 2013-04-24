# -*- coding: utf-8 *-*
import urllib2
import logging
import json
import random

from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from django.core.cache import cache
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

from django.contrib.contenttypes.models import ContentType

from django.views.base import View

from django.conf import settings


def plot_model_series_data(request, model_name, field_name, count):
    """"
    receive model name, field name and number of elements and returns the json
    response with required number of data points to plot the graph
    """
    #t = [tm.value for tm in list(TimeSeries.objects.all())[-30:]]
    #t = list(TimeSeries.objects.values_list('value', flat=True))[-100:]
    try:

        ct = ContentType.objects.get(model=model_name.lower())
        series = ct.model_class().objects.order_by('-id')[:count]

        try:
            t = [float(
                element.serializable_value(field_name))
                for element in series]
            t.reverse()
        except ValueError:
            t = 'Non-plottable values in the models.'

    except ContentType.DoesNotExist:
        t = 'Model or Field cannot be found.'
    response = {}
    for count, value in enumerate(t):
        response[count] = value
    # json data is just a JSON string now.
    json_data = json.dumps(response)
    return HttpResponse(json_data, mimetype="application/json")


def plot_redis_series_data(request, server_address, list_name, count):
    """
    Gets the server address listname and count to retrieve data points
    for the graph from the database
    """
    try:
        import redis
    except ImportError, e:
        logging.error("redis -redis server binding for Python \
                        is not installed.\
                        Try pip install redis")
    try:
        from redis import ConnectionError
        r_inst = redis.Redis(server_address)
        r_inst.ping()
    except ConnectionError:
        logging.error("redis server is not running. \
                    Start it to make graphos plot data.")
    data_list = r_inst.lrange(list_name, -int(count), -1)
    response = {}
    for count, value in enumerate(data_list):
        response[count] = value
    # json data is just a JSON string now.
    json_data = json.dumps(response)
    return HttpResponse(json_data, mimetype="application/json")


def plot_data(request):

    try:
        backend = request.GET['backend']
    except:
        backend = settings.GRAPHOS_DEFAULT_DATABASE

    if backend == 'model':
        from handlers.model_plot import ModelPlotDataHandler

        model_name = request.GET['model_name']
        field_name = request.GET['field_name']
        count = request.GET['count']

        try:
            site_id = request.GET['site_id']
        else:
            site_id = settings.SITE_ID

        data_obj = ModelPlotDataHandler(site_id, model_name, field_name, count)
        t = data_obj.get_data_instance()

        response = {}
        for count, value in enumerate(t):
            response[count] = value
        # json data is just a JSON string now.
        json_data = json.dumps(response)
        print json_data
        return HttpResponse(json_data, mimetype="application/json")

    # if bakend == 'mongodb':
    #     from handlers.mongo_plot import MongoPlotDataHandler as DataHandler
    #     data = MongoPlotDataHandler()
    # if backend == 'redis':
    #     from handlers.redis_plot import RedisPlotDataHandler as DataHandler
    #     data = RedisPlotDataHandler()
