from django.test import TestCase

from pymongo.errors import CollectionInvalid

from .sources.base import BaseDataSource
from .sources.simple import SimpleDataSource
from .sources.csv_file import CSVDataSource
from .sources.model import ModelDataSource
from .sources.mongo import MongoDBDataSource

from .renderers import base, flot, gchart, yui, matplotlib_renderer
from .exceptions import GraphosException
from .utils import DEFAULT_HEIGHT, DEFAULT_WIDTH, get_default_options, get_db

from demo.models import Account

import os
import json

current_path = os.path.dirname(os.path.abspath(__file__))


class TestSources(TestCase):
    def test_base_data_source(self):
        data_source = BaseDataSource()
        self.assertTrue(hasattr(data_source, "get_data"))
        self.assertRaises(GraphosException, data_source.get_data,)
        self.assertTrue(hasattr(data_source, "get_header"))
        self.assertRaises(GraphosException, data_source.get_header)
        self.assertTrue(hasattr(data_source, "get_first_column"))
        self.assertRaises(GraphosException, data_source.get_first_column)

    def test_simple_data_source(self):
        data = [
            ['Year', 'Sales', 'Expenses'],
            ['2004', 1000, 400],
            ['2005', 1170, 460],
            ['2006', 660, 1120],
            ['2007', 1030, 540]
        ]
        data_source = SimpleDataSource(data)
        self.assertEqual(data_source.get_data(), data)
        self.assertEqual(data_source.get_header(),
                         ['Year', 'Sales', 'Expenses'])
        self.assertEqual(data_source.get_first_column(),
                         ['2004', '2005', '2006', '2007'])

    def test_csv_data_source(self):
        data = [
            ['Year', 'Sales', 'Expense'],
            ['2006', '1000', '400'],
            ['2007', '1170', '460'],
            ['2008', '660', '1120'],
            ['2009', '1030', '540']
        ]
        csv_file = open(os.path.join(current_path, "test_data/accounts.csv"),
                        "r")
        data_source = CSVDataSource(csv_file)
        self.assertEqual(data, data_source.get_data())
        self.assertEqual(data_source.get_header(),
                         ['Year', 'Sales', 'Expense'])
        self.assertEqual(data_source.get_first_column(),
                         ['2006', '2007', '2008', '2009'])

    def test_model_data_source(self):
        data = [
            ['year', 'sales', 'expenses'],
            [u'2004', 1000, 400],
            [u'2005', 1170, 460],
            [u'2006', 660, 1120],
            [u'2007', 1030, 540]
        ]
        #Create some rows
        Account.objects.create(year="2004", sales=1000,
                               expenses=400, ceo="Welch")
        Account.objects.create(year="2005", sales=1170,
                               expenses=460, ceo="Jobs")
        Account.objects.create(year="2006", sales=660,
                               expenses=1120, ceo="Page")
        Account.objects.create(year="2007", sales=1030,
                               expenses=540, ceo="Welch")
        query_set = Account.objects.all()
        data_source = ModelDataSource(query_set, ['year', 'sales', 'expenses'])
        self.assertEqual(data, data_source.get_data())
        self.assertEqual(data_source.get_header(),
                         ['year', 'sales', 'expenses'])
        self.assertEqual(data_source.get_first_column(),
                         ['2004', '2005', '2006', '2007'])


def get_mongodb_test_db(db_name, collection_name):
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    test_data_file = open(cur_dir + '/test_data/mongodb/test_zips.json')
    db = get_db(db_name)
    try:
        db.create_collection(collection_name)
    except CollectionInvalid:
        pass
    for line in test_data_file:
        doc = json.loads(line)
        db[collection_name].save(doc)
    test_data_file.close()
    return db


class TestMongoDBSource(TestCase):

    def setUp(self):
        db_name = "test_db"
        collection_name = "zips"
        self.db = get_mongodb_test_db(db_name, collection_name)
        self.collection = self.db[collection_name]
        self.cursor = self.collection.find()
        self.fields = ['_id', 'pop']
        self.data = [['_id', 'pop'], ['35004', 6055], ['35005', 10616],
                     ['35006', 3205], ['35007', 14218], ['35010', 19942],
                     ['35014', 3062], ['35016', 13650], ['35019', 1781],
                     ['35020', 40549], ['35023', 39677], ['35031', 9058],
                     ['35033', 3448], ['35034', 3791], ['35035', 1282],
                     ['35040', 4675], ['35042', 4902], ['35043', 4781],
                     ['35044', 7985], ['35045', 13990], ['35049', '']]
        self.data_source = MongoDBDataSource(cursor=self.cursor,
                                             fields=self.fields)

    def test_data_source(self):
        self.assertTrue(hasattr(self.data_source, 'get_data'))
        self.assertTrue(hasattr(self.data_source, 'get_header'))
        self.assertTrue(hasattr(self.data_source, 'get_first_column'))
        self.assertEqual(self.data, self.data_source.get_data())
        self.assertEqual(self.fields, self.data_source.get_header())
        self.assertEqual(
            [el[0] for el in self.data[1:]],
            self.data_source.get_first_column()
        )

    def tearDown(self):
        self.db.drop_collection(self.collection.name)


class TestBaseRenderer(TestCase):

    def setUp(self):
        data = [
            ['Year', 'Sales', 'Expenses'],
            [2004, 1000, 400],
            [2005, 1170, 460],
            [2006, 660, 1120],
            [2007, 1030, 540]
        ]

        options = {"title": "Sales and Expences Graph"}

        self.default_options = {'title': 'Chart'}
        self.empty_options = {}
        self.data_source = SimpleDataSource(data)
        self.data = data
        self.options = options
        self.html_id = 'base_chart'
        self.template = 'graphos/as_html.html'
        self.header = data[0]

    def test_base_chart(self):
        chart = base.BaseChart(data_source=self.data_source,
                               options=self.options,
                               html_id=self.html_id)
        empty_options_chart = base.BaseChart(data_source=self.data_source,
                                             options=self.empty_options)
        self.assertTrue(hasattr(chart, "width"))
        self.assertEqual(DEFAULT_WIDTH, chart.width)
        self.assertTrue(hasattr(chart, "height"))
        self.assertEqual(DEFAULT_HEIGHT, chart.height)
        self.assertTrue(hasattr(chart, "header"))
        self.assertEqual(self.header, chart.header)
        self.assertTrue(hasattr(chart, "get_data"))
        self.assertEqual(self.data, chart.get_data())
        self.assertTrue(hasattr(chart, "get_data_json"))
        self.assertEqual(json.dumps(self.data), chart.get_data_json())
        self.assertTrue(hasattr(chart, "get_options"))
        self.assertEqual(self.options, chart.get_options())
        self.assertEqual(self.default_options,
                         empty_options_chart.get_options())
        self.assertTrue(hasattr(chart, "get_options_json"))
        self.assertEqual(json.dumps(self.options),
                         chart.get_options_json())
        self.assertTrue(hasattr(chart, "get_template"))
        self.assertEqual(self.template, chart.get_template())
        self.assertTrue(hasattr(chart, "get_html_template"))
        self.assertRaises(GraphosException, chart.get_html_template)
        self.assertTrue(hasattr(chart, "get_js_template"))
        self.assertRaises(GraphosException, chart.get_js_template)
        self.assertTrue(hasattr(chart, "get_html_id"))
        self.assertTrue(self.html_id, chart.get_html_id())
        self.assertTrue(hasattr(chart, "as_html"))


class TestFlotRenderer(TestCase):
    """ Test Cases for the graphos.renderers.flot module"""

    def setUp(self):
        data = [
            ['Year', 'Sales', 'Expenses'],
            [2004, 1000, 400],
            [2005, 1170, 460],
            [2006, 660, 1120],
            [2007, 1030, 540]
        ]
        self.data_source = SimpleDataSource(data)
        self.data = data
        self.options = {"title": "Sales and Expences Graph"}
        self.default_options = get_default_options()
        self.series_1 = [(2004, 1000), (2005, 1170), (2006, 660), (2007, 1030)]
        self.series_2 = [(2004, 400), (2005, 460), (2006, 1120), (2007, 540)]
        self.html_template = 'graphos/flot/html.html'
        self.js_template = 'graphos/flot/js.html'
        self.data_source = SimpleDataSource(data)
        self.data = data
        self.html_id = 'base_chart'
        self.header = data[0]
        series_object_1 = {'data': [(2004, 1000),
                                    (2005, 1170),
                                    (2006, 660),
                                    (2007, 1030)],
                           'label': 'Sales'}
        series_object_2 = {'data': [(2004, 400),
                                    (2005, 460),
                                    (2006, 1120),
                                    (2007, 540)],
                           'label': 'Expenses'}
        self.series_objects = [series_object_1, series_object_2]

    def test_base_flot_chart(self):
        chart = flot.BaseFlotChart(data_source=self.data_source,
                                   options=self.options)
        empty_options_chart = flot.BaseFlotChart(data_source=self.data_source,
                                                 options={})
        json_data = chart.get_serieses()
        self.assertEqual([self.series_1, self.series_2], json_data)
        self.assertEqual(self.html_template, chart.get_html_template())
        self.assertEqual(self.js_template, chart.get_js_template())
        default = get_default_options()
        self.assertEqual(default,
                         empty_options_chart.get_options())
        default.update(self.options)
        self.assertEqual(default, chart.get_options())
        self.assertEqual(json.dumps(default), chart.get_options_json())
        self.assertEqual(self.series_objects, chart.get_series_objects())
        self.assertEqual(json.dumps(self.series_objects),
                         chart.get_series_objects_json())

    def test_line_chart(self):
        chart = flot.LineChart(data_source=self.data_source,
                               options=self.options)
        empty_options_chart = flot.LineChart(data_source=self.data_source,
                                             options={})
        json_data = chart.get_serieses()
        self.assertEqual([self.series_1, self.series_2], json_data)
        default = get_default_options("lines")
        self.assertEqual(default,
                         empty_options_chart.get_options())
        default.update(self.options)
        self.assertEqual(default,
                         chart.get_options())

    def test_bar_chart(self):
        chart = flot.BarChart(data_source=self.data_source,
                              options=self.options)
        empty_options_chart = flot.BarChart(data_source=self.data_source,
                                            options={})
        json_data = chart.get_serieses()
        self.assertEqual([self.series_1, self.series_2], json_data)
        default = get_default_options("bars")
        self.assertEqual(default,
                         empty_options_chart.get_options())
        default.update(self.options)
        self.assertEqual(default,
                         chart.get_options())

    def test_point_chart(self):
        chart = flot.PointChart(data_source=self.data_source,
                                options=self.options)
        empty_options_chart = flot.PointChart(data_source=self.data_source,
                                              options={})
        json_data = chart.get_serieses()
        self.assertEqual([self.series_1, self.series_2], json_data)
        default = get_default_options("points")
        self.assertEqual(default,
                         empty_options_chart.get_options())
        default.update(self.options)
        self.assertEqual(default,
                         chart.get_options())


class TestGchartRenderer(TestCase):
    def setUp(self):
        data = [
            ['Year', 'Sales', 'Expenses'],
            [2004, 1000, 400],
            [2005, 1170, 460],
            [2006, 660, 1120],
            [2007, 1030, 540]
        ]
        self.data_source = SimpleDataSource(data)
        self.data = data

    def test_line_chart(self):
        chart = gchart.LineChart(data_source=self.data_source)
        self.assertNotEqual(chart.as_html(), "")
        self.assertTrue("LineChart" in chart.as_html())

    def test_column_chart(self):
        chart = gchart.ColumnChart(data_source=self.data_source)
        self.assertNotEqual(chart.as_html(), "")
        self.assertTrue("Column" in chart.as_html())

    def test_bar_chart(self):
        chart = gchart.BarChart(data_source=self.data_source)
        self.assertNotEqual(chart.as_html(), "")
        self.assertTrue("BarChart" in chart.as_html())

    def test_candlestick_chart(self):
        chart = gchart.CandlestickChart(data_source=self.data_source)
        self.assertNotEqual(chart.as_html(), "")
        self.assertTrue("CandlestickChart" in chart.as_html())

    def test_gauge_chart(self):
        chart = gchart.GaugeChart(data_source=self.data_source)
        self.assertNotEqual(chart.as_html(), "")
        self.assertTrue("Gauge" in chart.as_html())


class TestYUIRenderer(TestCase):
    def setUp(self):
        data = [
            ['Year', 'Sales', 'Expenses'],
            [2004, 1000, 400],
            [2005, 1170, 460],
            [2006, 660, 1120],
            [2007, 1030, 540]
        ]
        self.data_source = SimpleDataSource(data)
        self.data = data

    def test_line_chart(self):
        chart = yui.LineChart(data_source=self.data_source)
        self.assertNotEqual(chart.as_html(), "")
        self.assertTrue("line" in chart.as_html())


class TestMatplotlibRenderer(TestCase):
    def setUp(self):
        data = [['Year', 'Sales', 'Expenses', 'Items Sold', 'Net Profit'],
                ['2004', 1000, 400, 100, 600],
                ['2005', 1170, 460, 120, 310],
                ['2006', 660, 1120, 50, -460],
                ['2007', 1030, 540, 100, 200]]
        self.data_source = SimpleDataSource(data)
        self.data = data

    def test_line_chart(self):
        chart = matplotlib_renderer.LineChart(self.data_source)
        self.assertNotEqual(chart.as_html(), "")

    def test_bar_chart(self):
        chart = matplotlib_renderer.BarChart(self.data_source)
        self.assertNotEqual(chart.as_html(), "")
