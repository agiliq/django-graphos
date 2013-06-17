from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.views.generic.base import TemplateView

from graphos.renderers import gchart, yui, flot, morris, highcharts
from graphos.sources.simple import SimpleDataSource
from graphos.sources.mongo import MongoDBDataSource
from graphos.sources.model import ModelDataSource
from graphos.views import RendererAsJson

from .models import Account
from .utils import get_mongo_cursor
from .utils import (data, candlestick_data,
                    mongo_series_object_1, mongo_series_object_2,
                    create_demo_accounts, create_demo_mongo, get_db)
from .custom_charts import CustomGchart

import json
import time
import urllib2
import markdown
import datetime
import pymongo
from dateutil.parser import parse



class Demo(TemplateView):
    renderer = None

    def get_context_data(self, **kwargs):
        super_context = super(Demo, self).get_context_data(**kwargs)
        create_demo_accounts()
        queryset = Account.objects.all()
        data_source = ModelDataSource(queryset,
                                      fields=['year', 'sales'])
        simple_data_source = SimpleDataSource(data=data)
        line_chart = self.renderer.LineChart(data_source,
                                      options={'title': "Sales Growth"})
        column_chart = self.renderer.ColumnChart(SimpleDataSource(data=data),
                                          options={'title': "Sales/ Expense"})
        bar_chart = self.renderer.BarChart(data_source,
                                    options={'title': "Expense Growth"})
        pie_chart = self.renderer.PieChart(data_source)

        context = {
                "data_source": data_source,
                "simple_data_source": simple_data_source,
                "line_chart": line_chart,
                "column_chart": column_chart,
                'bar_chart': bar_chart,
                'pie_chart': pie_chart,
                }
        context.update(super_context)
        return context


def home(request):
    chart = flot.LineChart(SimpleDataSource(data=data), html_id="line_chart")
    g_chart = gchart.LineChart(SimpleDataSource(data=data))
    cursor = get_mongo_cursor("graphos_mongo",
                              "zips",
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


class GChartDemo(Demo):
    template_name = "demo/gchart.html"

    def get_context_data(self, **kwargs):
        context = super(GChartDemo, self).get_context_data(**kwargs)
        candlestick_chart = gchart.CandlestickChart(SimpleDataSource
                                                    (data=candlestick_data))
        context.update({'candlestick_chart': candlestick_chart})
        return context

gchart_demo = GChartDemo.as_view(renderer=gchart)

class YUIDemo(Demo):
    template_name = 'demo/yui.html'

yui_demo = YUIDemo.as_view(renderer=yui)


class MorrisDemo(TemplateView):
    template_name = 'demo/morris.html'
    renderer = None

    def get_context_data(self):
        create_demo_accounts()
        queryset = Account.objects.all()
        data_source = ModelDataSource(queryset,
                                      fields=['year', 'sales'])
        simple_data_source = SimpleDataSource(data=data)
        line_chart = self.renderer.LineChart(data_source,
                                      options={'title': "Sales Growth"})
        bar_chart = self.renderer.BarChart(data_source,
                                    options={'title': "Expense Growth"})
        donut_chart = self.renderer.DonutChart(data_source)
        context = {"line_chart": line_chart,
               'bar_chart': bar_chart,
               'donut_chart': donut_chart}
        return context


morris_demo = MorrisDemo.as_view(renderer=morris)


class FlotDemo(Demo):
    template_name = 'demo/flot.html'

    def get_context_data(self):
        context = super(FlotDemo, self).get_context_data()
        data_source = context["data_source"]
        point_chart = self.renderer.PointChart(data_source,
                                  options={'title': "Sales Growth"})
        context["point_chart"] = point_chart
        return context

flot_demo = FlotDemo.as_view(renderer=flot)

class HighChartsDemo(Demo):
    template_name = "demo/highcharts.html"

highcharts_demo = HighChartsDemo.as_view(renderer=highcharts)


def smart_date(value):

    if type(value) == datetime.datetime:
        return value

    if value == 'today':
        return datetime.datetime.now()
    elif value == 'yesterday':
        return datetime.datetime.now() - datetime.timedelta(days=1)
    elif value == 'tomorrow':
        return datetime.datetime.now() + datetime.timedelta(days=1)
    elif value == 'year_ago':
        return datetime.datetime.now() - datetime.timedelta(days=365)
    elif value == 'start_of_month':
        today = datetime.datetime.today()
        return datetime.datetime(today.year, today.month, 1)
    elif value == 'start_of_year':
        today = datetime.datetime.today()
        return datetime.datetime(today.year, 1, 1)
    else:
        return parse(value, dayfirst=True)


def get_query(start=None, end=None, query_filter=None):

    query = {}

    if start is not None:
        ts = int(time.mktime(smart_date(start).timetuple())) * 1000
        query = {'_id': {'$gt': '%s' % ts}}

    if end is not None:
        ts = int(time.mktime(smart_date(end).timetuple())) * 1000
        if query == {}:
            query = {'_id': {'$lt': '%s' % ts}}
        else:
            query = {'$and': [{'_id': {'$lt': '%s' % ts}}, query]}

    if query_filter is not None:
        query = {'$and': [{'_id': {'$regex': query_filter}}, query]}
    else:
        query = {'$and': [{'_id': {'$regex': 'all'}}, query]}

    return query


def build_timeseries_chart(period,
                           series,
                           start=None,
                           end=None):
    datasets = {}

    db = get_db('charts')
    data_source = []
    for i in range(len(series)):
        s = series[i]
        collection = "mapreduce_%s__%s__%s__%s" % (period,
                                                   s['mapreduce_function'],
                                                   s['resource'],
                                                   s['field'])
        new_series = []

        query = get_query(start, end, s['filter'])

        for rec in db[collection].find(query):
            key_timestamp = int(rec['_id'].split(':')[0]) / 10000
            new_series.append([key_timestamp, rec['value']])

        datasets[i] = {'data': new_series,
                       'label': "series %s: %s" % (i + 1, s['field'])}

        cursor = db[collection].find(query)
        data_source.append([(get_val_from_id(rec["_id"]),
                           rec['value']) for rec in cursor])

    return datasets


def get_val_from_id(id_):
    return int(id_.split(':')[0]) / 10000


class DemoMongoDBDataSource(MongoDBDataSource):

    def get_data(self):
        data = super(DemoMongoDBDataSource, self).get_data()
        new_data = [data[0]]
        for el in data[1:]:
            id_ = get_val_from_id(el[0])
            new_data.append([id_, el[1]])
        return new_data


def time_series_demo(request):
    create_demo_mongo()
    db = get_db('charts')

    query = get_query('year_ago', None,
                      'employee=/example/employee/500ff1b8e147f74f7000000c/')
    coll_name = "mapreduce_daily__sumof__time_record__hours"
    cursor = db[coll_name].find(query)
    data_source_2 = DemoMongoDBDataSource(cursor, fields=["_id", "value"])
    chart_2 = flot.LineChart(data_source_2)

    accounts_cursor = get_db("accounts").docs.find()
    data_source_3 = MongoDBDataSource(accounts_cursor,
                                      fields=['Year', 'Sales', 'Expenses'])

    chart_3 = gchart.LineChart(data_source_3)
    period = 'weekly'
    start = 'year_ago'
    end = None
    series = [
        {'resource': 'time_record',
         'field': 'hours',
         'filter': 'employee=/example/employee/500ff1b8e147f74f7000000c/',
         'mapreduce_function': 'sumof'},

        {'resource': 'other_time_record',
         'field': 'hours',
         'filter': 'employee=/example/employee/500ff1b8e147f74f7000000c/',
         'mapreduce_function': 'sumof'}]

    datasets = build_timeseries_chart(period=period,
                                      series=series,
                                      start=start,
                                      end=end)

    context = {'datasets': json.dumps(datasets),
               'chart_2': chart_2,
               "chart_3": chart_3
               }
    return render(request, 'demo/mongodb_source.html', context)

class GhcartRendererAsJson(RendererAsJson):

    def get_context_data(self):
        create_demo_accounts()
        Account.objects.create(year="2010", sales=2130,
                               expenses=1940, ceo="Cook")
        queryset = Account.objects.all()
        data_source = ModelDataSource(queryset,
                                      fields=['year', 'sales'])
        line_chart = gchart.LineChart(data_source)
        context = {"chart": line_chart}
        return context

custom_gchart_renderer = GhcartRendererAsJson.as_view()
