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
    return render(request, 'demo/home.html', {'chart': chart,
                                              'g_chart': g_chart},)


def tutorial(request):
    chart = LineChart(SimpleDataSource(data=data), html_id="line_chart")
    return render(request, 'demo/tutorial.html', {'chart': chart}, )


def gchart_demo(request):
    line_chart = gchart.LineChart(SimpleDataSource(data=data))
    column_chart = gchart.ColumnChart(SimpleDataSource(data=data))
    bar_chart = gchart.BarChart(SimpleDataSource(data=data))
    context = {"line_chart": line_chart, "column_chart": column_chart,
               'bar_chart': bar_chart}
    return render(request, 'demo/gchart.html', context)
