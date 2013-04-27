from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from graphos.renderers.flot import LineChart
from graphos.renderers import gchart
from graphos.sources.simple import SimpleDataSource


def home(request):
    data =  [
            ['Year', 'Sales', 'Expenses'],
            [2004, 1000, 400],
            [2005, 1170, 460],
            [2006, 660, 1120],
            [2007, 1030, 540]
            ]

    chart = LineChart(SimpleDataSource(data=data), html_id="line_chart")
    g_chart = gchart.LineChart(SimpleDataSource(data=data))
    c = RequestContext(request)
    return render_to_response('home.html', {'chart': chart,
                                            'g_chart': g_chart},
                              context_instance=c)

def tutorial(request):
    data =  [
            ['Year', 'Sales', 'Expenses'],
            [2004, 1000, 400],
            [2005, 1170, 460],
            [2006, 660, 1120],
            [2007, 1030, 540]
        ]
    chart = LineChart(SimpleDataSource(data=data), html_id="line_chart")
    c = RequestContext(request,)
    return render_to_response('tutorial.html', {'chart': chart}, context_instance=c)

