import urllib2
import logging
import json
import random

from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from django.core.cache import cache
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect, HttpResponseNotModified, \
                        HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from graphos.core.models import TimeSeries


@csrf_exempt
def home(request):
    """
    Try a POST with curl and automatically adds a random value, this updates plot async"""
    if request.POST:
        TimeSeries.objects.create(value=random.randrange(0, 10))
    c = RequestContext(request, {

    })
    return render_to_response('home.html', context_instance=c)


def plot_data(request):
    #t = [tm.value for tm in list(TimeSeries.objects.all())[-30:]]
    t = list(TimeSeries.objects.values_list('value', flat=True))[-30:]
    response = {}
    for count, value in enumerate(t):
        response[count] = value
    # json data is just a JSON string now.
    json_data = json.dumps(response)
    return HttpResponse(json_data, mimetype="application/json")
