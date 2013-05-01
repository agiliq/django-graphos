from django.shortcuts import render
from django.views.decorators.cache import cache_page

from graphos.renderers import gchart, yui, flot
from graphos.sources.simple import SimpleDataSource
from graphos.sources.mongo import MongoDBDataSource
from graphos.sources.model import ModelDataSource

from .models import Account

from .utils import get_mongo_cursor

import markdown
import urllib2

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


def create_demo_accounts():
    Account.objects.all().delete()
    #Create some rows
    Account.objects.create(year="2004", sales=1000,
                           expenses=400, ceo="Welch")
    Account.objects.create(year="2005", sales=1170,
                           expenses=460, ceo="Jobs")
    Account.objects.create(year="2006", sales=660,
                           expenses=1120, ceo="Page")
    Account.objects.create(year="2007", sales=1030,
                           expenses=540, ceo="Welch")
    Account.objects.create(year="2008", sales=2030,
                           expenses=1540, ceo="Zuck")
    Account.objects.create(year="2009", sales=2230,
                           expenses=1840, ceo="Cook")


def home(request):
    chart = flot.LineChart(SimpleDataSource(data=data), html_id="line_chart")
    g_chart = gchart.LineChart(SimpleDataSource(data=data))
    cursor = get_mongo_cursor(db_name="graphos_mongo",
                              collection_name="zips",
                              max_docs=100)
    m_data = MongoDBDataSource(cursor=cursor, fields=['_id', 'pop'])
    m_chart = flot.LineChart(m_data)

    context = {'chart': chart,
               'g_chart': g_chart,
               'm_chart': m_chart}
    return render(request, 'demo/home.html', context)


@cache_page
def tutorial(request):
    chart = flot.LineChart(SimpleDataSource(data=data), html_id="line_chart")
    url = "https://raw.github.com/agiliq/django-graphos/master/README.md"
    str = urllib2.urlopen(url).read()
    readme = markdown.markdown(str)
    context = {'chart': chart, "readme": readme}
    return render(request, 'demo/tutorial.html', context)


def gchart_demo(request):
    create_demo_accounts()
    queryset = Account.objects.all()
    data_source = ModelDataSource(queryset,
                                  fields=['year', 'sales'])
    line_chart = gchart.LineChart(data_source,
                                  options={'title': "Sales Growth"})
    column_chart = gchart.ColumnChart(SimpleDataSource(data=data),
                                      options={'title': "Sales vs Expense"})
    bar_chart = gchart.BarChart(data_source,
                                options={'title': "Expense Growth"})
    candlestick_chart = gchart.CandlestickChart(SimpleDataSource
                                                (data=candlestick_data))
    pie_chart = gchart.PieChart(data_source)
    context = {"line_chart": line_chart, "column_chart": column_chart,
               'bar_chart': bar_chart, 'candlestick_chart': candlestick_chart,
               'pie_chart': pie_chart}
    return render(request, 'demo/gchart.html', context)


def yui_demo(request):
    line_chart = yui.LineChart(SimpleDataSource(data=data))
    context = {"line_chart": line_chart}
    return render(request, 'demo/yui.html', context)


def flot_demo(request):
    create_demo_accounts()
    queryset = Account.objects.all()
    data_source = ModelDataSource(queryset,
                                  fields=['year', 'sales'])
    line_chart = flot.LineChart(data_source,
                                options={'title': "Sales Growth"})
    bar_chart = flot.BarChart(data_source,
                              options={'title': "Sales Growth"})
    point_chart = flot.PointChart(data_source,
                                  options={'title': "Sales Growth"})
    context = {'line_chart': line_chart,
               'bar_chart': bar_chart,
               'point_chart': point_chart}
    return render(request, 'demo/flot.html', context)
