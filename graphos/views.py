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


def plot_model_data(request, model_name, field_name, count):
    #t = [tm.value for tm in list(TimeSeries.objects.all())[-30:]]
    #t = list(TimeSeries.objects.values_list('value', flat=True))[-100:]
    try:
        ct = ContentType.objects.get(model=model_name.lower())
        series = ct.model_class().objects.order_by('-id')[:count]
        try:
            t = [float(element.serializable_value(field_name)) for element in series]
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
