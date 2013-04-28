from django.shortcuts import render

from graphos.renderers.base import BaseChart
from graphos.renderers.flot import LineChart
from graphos.renderers import gchart, yui
from graphos.sources.simple import SimpleDataSource
from graphos.sources.mongo import MongoDBDataSource

data = [
       ['Year', 'Sales', 'Expenses'],
       ['2004', 1000, 400],
       ['2005', 1170, 460],
       ['2006', 660, 1120],
       ['2007', 1030, 540]]

candlestick_data = [['Mon', 20, 28, 38, 45],
                    ['Tue', 31, 38, 55, 66],
                    ['Wed', 50, 55, 77, 80],
                    ['Thu', 77, 77, 66, 50],
                    ['Fri', 68, 66, 22, 15]]

mongo_series_object_1 = [[440, 39],
                         [488, 29.25],
                         [536, 28],
                         [584, 29],
                         [632, 33.25],
                         [728, 28.5],
                         [776, 33.25],
                         [824, 28.5],
                         [872, 31],
                         [920, 30.75],
                         [968, 26.25]]

mongo_series_object_2 = [[400, 4],
                         [488, 0],
                         [536, 20],
                         [584, 8],
                         [632, 2],
                         [680, 36],
                         [728, 0],
                         [776, 0],
                         [824, 0],
                         [872, 4],
                         [920, 1],
                         [968, 0]]

mongo_data = [{'data': mongo_series_object_1, 'label': 'hours'},
              {'data': mongo_series_object_2, 'label': 'hours'}]


def home(request):
    chart = LineChart(SimpleDataSource(data=data), html_id="line_chart")
    g_chart = gchart.LineChart(SimpleDataSource(data=data))
    m_chart = BaseChart(data_source=MongoDBDataSource(data=mongo_data),
                        html_id='mongo_chart')

    context = {'chart': chart,
               'g_chart': g_chart,
               'm_chart': m_chart}
    return render(request, 'demo/home.html', context)


def tutorial(request):
    chart = LineChart(SimpleDataSource(data=data), html_id="line_chart")
    return render(request, 'demo/tutorial.html', {'chart': chart}, )


def gchart_demo(request):
    line_chart = gchart.LineChart(SimpleDataSource(data=data))
    column_chart = gchart.ColumnChart(SimpleDataSource(data=data))
    bar_chart = gchart.BarChart(SimpleDataSource(data=data))
    candlestick_chart = gchart.CandlestickChart(SimpleDataSource
                                                (data=candlestick_data))
    context = {"line_chart": line_chart, "column_chart": column_chart,
               'bar_chart': bar_chart, 'candlestick_chart': candlestick_chart}
    return render(request, 'demo/gchart.html', context)


def yui_demo(request):
    line_chart = yui.LineChart(SimpleDataSource(data=data))
    context = {"line_chart": line_chart}
    return render(request, 'demo/yui.html', context)
