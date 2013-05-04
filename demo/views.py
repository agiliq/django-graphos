from django.shortcuts import render
from django.views.decorators.cache import cache_page

from graphos.renderers import gchart, yui, flot
from graphos.sources.simple import SimpleDataSource
from graphos.sources.mongo import MongoDBDataSource
from graphos.sources.model import ModelDataSource

from .models import Account
from .utils import get_mongo_cursor

import json
import time
import urllib2
import markdown
import datetime
import pymongo
from dateutil.parser import parse

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

def create_demo_mongo():
    accounts = get_db("accounts")
    docs = accounts.docs
    docs.drop

    docs = accounts.docs
    header = data[0]
    data_only = data[1:]
    for row in data_only:
        docs.insert(dict(zip(header, row)))


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


def get_db(db_name):
    DB_HOST = ["localhost"]
    DB_PORT = 27017
    db = pymongo.Connection(DB_HOST, DB_PORT)[db_name]
    return db


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
                       'label': s['field']}

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
    coll_name = "mapreduce_daily__sumof__time_record__hours"
    query = get_query('year_ago', None,
                      'employee=/example/employee/500ff1b8e147f74f7000000c/')
    cursor = db[coll_name].find(query)
    data_source_2 = DemoMongoDBDataSource(cursor, fields=["_id", "value"])
    chart = flot.LineChart(data_source_2)

    accounts_cursor = get_db("accounts").docs.find()
    data_source_3 = MongoDBDataSource(accounts_cursor,
                                      fields=['Year', 'Sales', 'Expenses'])
    chart_2 = gchart.LineChart(data_source_3)
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

    context = {'datasets': json.dumps(datasets), 'chart': chart, "chart_2": chart_2}
    return render(request, 'demo/mongodb_source.html', context)
