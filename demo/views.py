from django.shortcuts import render

from graphos.renderers.flot import LineChart
from graphos.renderers import gchart
from graphos.sources.simple import SimpleDataSource

data = [
       ['Year', 'Sales', 'Expenses'],
       [2004, 1000, 400],
       [2005, 1170, 460],
       [2006, 660, 1120],
       [2007, 1030, 540], ]


def home(request):
    chart = LineChart(SimpleDataSource(data=data), html_id="line_chart")
    g_chart = gchart.LineChart(SimpleDataSource(data=data))
    return render(request, 'home.html', {'chart': chart,
                                         'g_chart': g_chart},
                  )


def tutorial(request):
    chart = LineChart(SimpleDataSource(data=data), html_id="line_chart")
    return render(request, 'tutorial.html', {'chart': chart}, )
