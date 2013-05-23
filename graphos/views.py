from django.views.generic.base import View
from django.http import HttpResponse

import json


class RendererAsJson(View):
    "A view which is used to get a chart as json."
    "Subclasses should create get_context_data, which populates a chart"
    def get(self, *args, **kwargs):
        context = self.get_context_data()
        chart = context["chart"]
        return HttpResponse(json.dumps(chart.get_data()))
