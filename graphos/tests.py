from django.test import TestCase

from pymongo.errors import CollectionInvalid

from .sources.base import BaseDataSource
from .sources.simple import SimpleDataSource
from .sources.csv_file import CSVDataSource
from .sources.model import ModelDataSource
from .sources.mongo import MongoDBDataSource

from .renderers import base, flot, gchart, yui, matplotlib_renderer, highcharts
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

        self.options = {"title": "Sales and Expences Graph"}

        self.default_options = {'title': 'Chart'}
        self.empty_options = {}
        self.data_source = SimpleDataSource(data)
        self.data = data
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
        self.assertRaises(GraphosException, chart.as_html)

    def test_options(self):
        """
        Assert that options get set to a dictionary in case no options is passed during initialization
        """
        chart = base.BaseChart(data_source=self.data_source)
        self.assertEqual(self.default_options, chart.get_options())


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
        self.assertTrue("ColumnChart" in chart.as_html())

    def test_bar_chart(self):
        chart = gchart.BarChart(data_source=self.data_source)
        self.assertNotEqual(chart.as_html(), "")
        self.assertTrue("BarChart" in chart.as_html())

    def test_pie_chart(self):
        chart = gchart.PieChart(data_source=self.data_source)
        self.assertNotEqual(chart.as_html(), "")
        self.assertTrue("PieChart" in chart.as_html())

    def test_area_chart(self):
        chart = gchart.AreaChart(data_source=self.data_source)
        self.assertNotEqual(chart.as_html(), "")
        self.assertTrue("AreaChart" in chart.as_html())

    def test_candlestick_chart(self):
        # TODO: Change tests. Candlestick probably expects data in a particular format.
        # Assert that data sent to candlestick is in correct format, and test accordingly
        chart = gchart.CandlestickChart(data_source=self.data_source)
        self.assertNotEqual(chart.as_html(), "")
        self.assertTrue("CandlestickChart" in chart.as_html())

    def test_gauge_chart(self):
        # TODO: Change tests. Candlestick probably expects data in a particular format.
        # Assert that data sent to candlestick is in correct format, and test accordingly
        chart = gchart.GaugeChart(data_source=self.data_source)
        self.assertNotEqual(chart.as_html(), "")
        self.assertTrue("Gauge" in chart.as_html())


class TestBaseHighcharts(TestCase):
    chart_klass = highcharts.BaseHighCharts

    def setUp(self):
        data = [
            ['Year', 'Sales', 'Expenses'],
            [2004, 1000, 400],
            [2005, 1170, 460],
            [2006, 660, 1120],
            [2007, 1030, 540]
        ]
        self.data_source = SimpleDataSource(data)
        self.categories = [2004, 2005, 2006, 2007]
        self.x_axis_title = 'Year'
        self.series = [{'name': 'Sales', 'data': [1000, 1170, 660, 1030]}, {'name': 'Expenses', 'data': [400, 460, 1120, 540]}]

    def test_get_categories(self):
        chart = self.chart_klass(data_source=self.data_source)
        self.assertEqual(chart.get_categories(), self.categories)
        self.assertEqual(chart.get_categories_json(), json.dumps(self.categories))


    def test_get_series(self):
        chart = self.chart_klass(data_source=self.data_source)
        self.assertEqual(chart.get_series(), self.series)

    def test_get_series_with_colors(self):
        chart = self.chart_klass(data_source=self.data_source, options={'colors': ['red']})
        series = [{'name': 'Sales', 'data': [1000, 1170, 660, 1030], 'color': 'red'}, {'name': 'Expenses', 'data': [400, 460, 1120, 540]}]
        self.assertEqual(chart.get_series(), series)
        chart = self.chart_klass(data_source=self.data_source, options={'colors': ['red', 'blue']})
        series = [{'name': 'Sales', 'data': [1000, 1170, 660, 1030], 'color': 'red'}, {'name': 'Expenses', 'data': [400, 460, 1120, 540], 'color': 'blue'}]
        self.assertEqual(chart.get_series(), series)

    def test_get_title(self):
        chart = self.chart_klass(data_source=self.data_source)
        self.assertEqual(chart.get_title(), {'text': 'Chart'})
        chart = self.chart_klass(data_source=self.data_source, options={'title': 'Highcharts'})
        self.assertEqual(chart.get_title(), {'text': 'Highcharts'})
        chart = self.chart_klass(data_source=self.data_source, options={'title': {'text': 'Highcharts', 'align': 'center'}})
        self.assertEqual(chart.get_title(), {'text': 'Highcharts', 'align': 'center'})

    def test_get_subtitle(self):
        chart = self.chart_klass(data_source=self.data_source)
        self.assertEqual(chart.get_subtitle(), {})
        chart = self.chart_klass(data_source=self.data_source, options={'subtitle': 'Highcharts'})
        self.assertEqual(chart.get_subtitle(), {'text': 'Highcharts'})
        chart = self.chart_klass(data_source=self.data_source, options={'subtitle': {'text': 'Highcharts', 'align': 'center'}})
        self.assertEqual(chart.get_subtitle(), {'text': 'Highcharts', 'align': 'center'})

    def test_get_xaxis(self):
        chart = self.chart_klass(data_source=self.data_source)
        self.assertEqual(chart.get_x_axis(), {'categories':self.categories, 'title': {'text': self.x_axis_title}})
        chart = self.chart_klass(data_source=self.data_source, options={'xAxis': {'type': 'logarithmic', 'title': {'text': 'Sales vs Year'}}})
        self.assertEqual(chart.get_x_axis(), {'categories':self.categories, 'title': {'text': 'Sales vs Year'}, 'type': 'logarithmic'})

    def test_get_yaxis(self):
        chart = self.chart_klass(data_source=self.data_source)
        self.assertEqual(chart.get_y_axis(), {'title': {'text': 'Values'}})

    def test_get_yaxis_single_series(self):
        single_data = [
            ['Year', 'Sales'],
            [2004, 1000],
            [2005, 1170],
            [2006, 660],
            [2007, 1030]
        ]
        chart = self.chart_klass(data_source=SimpleDataSource(single_data))
        self.assertEqual(chart.get_y_axis(), {'title': {'text': 'Sales'}})

    def test_get_tooltip(self):
        chart = self.chart_klass(data_source=self.data_source)
        self.assertEqual(chart.get_tooltip(), {})

    def test_get_credits(self):
        chart = self.chart_klass(data_source=self.data_source)
        self.assertEqual(chart.get_credits(), {})

    def test_get_exporting(self):
        chart = self.chart_klass(data_source=self.data_source)
        self.assertEqual(chart.get_exporting(), {})

    def test_get_legend(self):
        chart = self.chart_klass(data_source=self.data_source)
        self.assertEqual(chart.get_legend(), {})

    def test_get_navigation(self):
        chart = self.chart_klass(data_source=self.data_source)
        self.assertEqual(chart.get_navigation(), {})


class TestHighchartsLineChart(TestBaseHighcharts):
    chart_klass = highcharts.LineChart

    def test_line_chart(self):
        chart = self.chart_klass(data_source=self.data_source)
        self.assertEqual(chart.get_chart(), {'type': 'line'})
        self.assertNotEqual(chart.as_html(), "")


class TestHighchartsBarChart(TestBaseHighcharts):
    chart_klass = highcharts.BarChart

    def test_bar_chart(self):
        chart = self.chart_klass(data_source=self.data_source)
        self.assertEqual(chart.get_chart(), {'type': 'bar'})
        self.assertNotEqual(chart.as_html(), "")


class TestHighchartsColumnChart(TestBaseHighcharts):
    chart_klass = highcharts.ColumnChart

    def test_column_chart(self):
        chart = self.chart_klass(data_source=self.data_source)
        self.assertEqual(chart.get_chart(), {'type': 'column'})
        self.assertNotEqual(chart.as_html(), "")


class TestHighchartsAreaChart(TestBaseHighcharts):
    chart_klass = highcharts.AreaChart

    def test_area_chart(self):
        chart = self.chart_klass(data_source=self.data_source)
        self.assertEqual(chart.get_chart(), {'type': 'area'})
        self.assertNotEqual(chart.as_html(), "")


class TestHighchartsPieChart(TestBaseHighcharts):
    chart_klass = highcharts.PieChart

    def test_pie_chart(self):
        chart = self.chart_klass(data_source=self.data_source)
        self.assertEqual(chart.get_chart(), {'type': 'pie'})
        self.assertNotEqual(chart.as_html(), "")

    def test_get_series(self):
        chart = self.chart_klass(data_source=self.data_source)
        series = [
            {'name': "Sales", "data": [{"name": 2004, "y": 1000}, {'name': 2005, 'y': 1170}, {'name': 2006, 'y': 660},
                                       {'name': 2007, 'y': 1030}]},
            {'name': 'Expenses', 'data': [{"name": 2004, "y": 400}, {'name': 2005, 'y': 460}, {'name': 2006, 'y': 1120},
                                          {'name': 2007, 'y': 540}]}
        ]
        self.assertEqual(chart.get_series(), series)

    # This function should be modified when color ability is added to Piechart.
    def test_get_series_with_colors(self):
        chart = self.chart_klass(data_source=self.data_source, options={'colors': ['red']})
        series = [
            {'name': "Sales", "data": [{"name": 2004, "y": 1000}, {'name': 2005, 'y': 1170}, {'name': 2006, 'y': 660},
                                       {'name': 2007, 'y': 1030}]},
            {'name': 'Expenses', 'data': [{"name": 2004, "y": 400}, {'name': 2005, 'y': 460}, {'name': 2006, 'y': 1120},
                                          {'name': 2007, 'y': 540}]}
        ]
        self.assertEqual(chart.get_series(), series)


class TestHighchartsScatterChart(TestBaseHighcharts):
    chart_klass = highcharts.ScatterChart
    multiseriesdata = [
        ['State', 'Country', 'Rainfall', 'Precipitation'],
        ['Uttar Pradesh', 'India', 1, 2],
        ['Bihar', 'India', 2, 3],
        ['Telangana', 'India', 5, 7],
        ['Lahore', 'Pakistan', 9, 8],
        ['Hyderabad', 'Pakistan', 8, 7],
        ['Lahore', 'Pakistan', 3, 11]
    ]

    def test_scatter_chart(self):
        chart = self.chart_klass(data_source=self.data_source)
        self.assertEqual(chart.get_chart(), {'type': 'scatter'})
        self.assertNotEqual(chart.as_html(), "")

    def test_get_series(self):
        chart = self.chart_klass(data_source=self.data_source)
        series = [{'data': [{'Year': 2004, 'x': 1000, 'y': 400}, {'Year': 2005, 'x': 1170, 'y': 460},
                            {'Year': 2006, 'x': 660, 'y': 1120}, {'Year': 2007, 'x': 1030, 'y': 540}],
                   'name': 'Year'}]
        self.assertEqual(chart.get_series(), series)
        # Scatter Chart has ability to work with multiseries data.
        chart = self.chart_klass(data_source=SimpleDataSource(self.multiseriesdata))
        series = [{"data": [{"y": 8, "x": 9, "State": "Lahore"}, {"y": 7, "x": 8, "State": "Hyderabad"}, {"y": 11, "x": 3, "State": "Lahore"}], "name": "Pakistan"}, {"data": [{"y": 2, "x": 1, "State": "Uttar Pradesh"}, {"y": 3, "x": 2, "State": "Bihar"}, {"y": 7, "x": 5, "State": "Telangana"}], "name": "India"}]
        self.assertEqual(chart.get_series(), series)

    # This function should be modified when color ability is added to Scatter.
    def test_get_series_with_colors(self):
        chart = self.chart_klass(data_source=self.data_source, options={'colors': ['red']})
        pass

    def test_get_xaxis(self):
        chart = self.chart_klass(data_source=self.data_source)
        self.assertEqual(chart.get_x_axis(),{'title': {'text': 'Sales'}})

    def test_get_yaxis(self):
        chart = self.chart_klass(data_source=self.data_source)
        self.assertEqual(chart.get_y_axis(), {'title': {'text': 'Expenses'}})

    def test_get_yaxis_single_series(self):
        pass


class TestHighchartsColumnLineChart(TestBaseHighcharts):
    chart_klass = highcharts.ColumnLineChart

    def test_line_chart(self):
        chart = self.chart_klass(data_source=self.data_source)
        self.assertEqual(chart.get_chart(), {'type': 'column_line'})
        self.assertNotEqual(chart.as_html(), "")

    def test_get_series(self):
        chart = self.chart_klass(data_source=self.data_source)
        series = [{'type': 'column', 'data': [1000, 1170, 660, 1030], 'name': 'Sales'},{'data': [400, 460, 1120, 540], 'name': 'Expenses', 'type': 'line'}]
        self.assertEqual(chart.get_series(), series)

    # This function should be modified when color ability is added to ColumnLine.
    def test_get_series_with_colors(self):
        chart = self.chart_klass(data_source=self.data_source, options={'colors': ['red']})
        series = [{'type': 'column', 'data': [1000, 1170, 660, 1030], 'name': 'Sales'},{'data': [400, 460, 1120, 540], 'name': 'Expenses', 'type': 'line'}]
        self.assertEqual(chart.get_series(), series)


class TestHighchartsLineColumnChart(TestBaseHighcharts):
    chart_klass = highcharts.LineColumnChart

    def test_line_chart(self):
        chart = self.chart_klass(data_source=self.data_source)
        self.assertEqual(chart.get_chart(), {'type': 'line_column'})
        self.assertNotEqual(chart.as_html(), "")

    def test_get_series(self):
        chart = self.chart_klass(data_source=self.data_source)
        series = [{'type': 'line', 'data': [1000, 1170, 660, 1030], 'name': 'Sales'},{'data': [400, 460, 1120, 540], 'name': 'Expenses', 'type': 'column'}]
        self.assertEqual(chart.get_series(), series)

    # This function should be modified when color ability is added to ColumnLine.
    def test_get_series_with_colors(self):
        chart = self.chart_klass(data_source=self.data_source, options={'colors': ['red']})
        series = [{'type': 'line', 'data': [1000, 1170, 660, 1030], 'name': 'Sales'},{'data': [400, 460, 1120, 540], 'name': 'Expenses', 'type': 'column'}]
        self.assertEqual(chart.get_series(), series)


class TestHighchartsFunnel(TestBaseHighcharts):
    chart_klass = highcharts.Funnel
    funnel_data = [['Unique users', 'Counts'],
                   ['Website visits', 654],
                   ['Downloads', 4064],
                   ['Requested price list', 1987],
                   ['Invoice sent', 976],
                   ['Finalized', 846]
                   ]

    def test_funnel_chart(self):
        chart = self.chart_klass(data_source=self.data_source)
        self.assertEqual(chart.get_chart(), {'type': 'funnel'})
        self.assertNotEqual(chart.as_html(), "")

    def test_get_series(self):
        chart = self.chart_klass(data_source=SimpleDataSource(self.funnel_data))
        series = [{'data': [['Website visits', 654], ['Downloads', 4064], ['Requested price list', 1987],
                            ['Invoice sent', 976], ['Finalized', 846]]}]
        self.assertEqual(chart.get_series(), series)

    # Needs to be modified when color functionality is added to Funnel
    def test_get_series_with_colors(self):
        chart = self.chart_klass(data_source=SimpleDataSource(self.funnel_data))
        series = [{'data': [['Website visits', 654],['Downloads', 4064],['Requested price list', 1987],['Invoice sent', 976],['Finalized', 846]]}]
        self.assertEqual(chart.get_series(), series)


class TestHighchartsBubbleChart(TestBaseHighcharts):
    chart_klass = highcharts.Bubble
    def setUp(self):
        data = [["Country", "Sugar Consumption", "Fat Consumption", "GDP"],
                ["India", 10, 15, 90],
                ["USA", 11, 20, 19],
                ["Srilanka", 15, 5, 98],
                ["Indonesia", 16, 35, 150]]
        self.data_source = SimpleDataSource(data)

    def test_bubble_chart(self):
        chart = self.chart_klass(data_source=self.data_source)
        self.assertEqual(chart.get_chart(), {'type': 'bubble'})
        self.assertNotEqual(chart.as_html(), "")

    def test_get_series(self):
        bubble_chart_data_multi = [["Grade", "Country", "Sugar Consumption", "Fat Consumption", "GDP"],
                                   ["A", "India", 10, 15, 90],
                                   ["B", "India", 11, 20, 19],
                                   ["P", "USA", 39, 21, 100],
                                   ["O", "USA", 44, 29, 150]]
        chart = self.chart_klass(data_source=self.data_source)
        series = [{'data': [{'y': 15, 'Country': 'India', 'z': 90, 'x': 10}, {'y': 20, 'Country': 'USA', 'z': 19, 'x': 11}, {'y': 5, 'Country': 'Srilanka', 'z': 98, 'x': 15}, {'y': 35, 'Country': 'Indonesia', 'z': 150, 'x': 16}], 'name': 'Country'}]
        self.assertEqual(chart.get_series(), series)
        chart = self.chart_klass(data_source=SimpleDataSource(bubble_chart_data_multi))
        series = [{'data': [{'Grade': 'A', 'x': 10, 'z': 90, 'y': 15}, {'Grade': 'B', 'x': 11, 'z': 19, 'y': 20}], 'name': 'India'}, {'data': [{'Grade': 'P', 'x': 39, 'z': 100, 'y': 21}, {'Grade': 'O', 'x': 44, 'z': 150, 'y': 29}], 'name': 'USA'}]
        self.assertEqual(chart.get_series(), series)

    # Needs to be modified when color functionality is added to Bubble
    def test_get_series_with_colors(self):
        pass

    def test_get_yaxis(self):
        chart = self.chart_klass(data_source=self.data_source)
        self.assertEqual(chart.get_y_axis(), {'title': {'text': 'Fat Consumption'}})

    def test_get_xaxis(self):
        chart = self.chart_klass(data_source=self.data_source)
        self.assertEqual(chart.get_x_axis(), {'title': {'text': 'Sugar Consumption'}})

    # Bubble chart do not have any attribute categories.
    def test_get_categories(self):
        pass

    # Bubble chart do not have any attribute yaxis singleseries.
    def test_get_yaxis_single_series(self):
        pass

class TestHighchartsHeatMap(TestBaseHighcharts):
    chart_klass = highcharts.HeatMap

    def test_heatmap_chart(self):
        chart = self.chart_klass(data_source=self.data_source)
        self.assertEqual(chart.get_chart(), {'type': 'heatmap'})
        self.assertNotEqual(chart.as_html(), "")

    def test_get_series(self):
        chart = self.chart_klass(data_source=self.data_source)
        series = [{'data': [[0, 0, 1000], [0, 1, 400], [1, 0, 1170], [1, 1, 460], [2, 0, 660], [2, 1, 1120], [3, 0, 1030], [3, 1, 540]]}]
        self.assertEqual(chart.get_series(), series)

    def test_get_yaxis(self):
        chart = self.chart_klass(data_source=self.data_source)
        self.assertEqual(chart.get_y_axis(), {'categories': ['Sales', 'Expenses']})

    # This function should be modified when color ability is added to Heatmap.
    def test_get_series_with_colors(self):
        pass

    def test_get_color_axis(self):
        chart = self.chart_klass(data_source=self.data_source)
        self.assertEqual(chart.get_color_axis(), {})

    def test_get_yaxis_single_series(self):
        pass


class TestHighchartsTreeMap(TestBaseHighcharts):
    chart_klass = highcharts.TreeMap
    treemap_data = [["Country", "Cause", "Death Rate"],
                    ["India", "Cardiovascular Disease", 10],
                    ["India", "Road Accident", 5],
                    ["China", "Cardiovascular Disease", 9],
                    ["China", "Road Accident", 6],
                    ]

    def test_treemap_chart(self):
        chart = self.chart_klass(data_source=SimpleDataSource(self.treemap_data))
        self.assertEqual(chart.get_chart(), {'type': 'treemap'})
        self.assertNotEqual(chart.as_html(), "")

    def test_get_series(self):
        chart = self.chart_klass(data_source=SimpleDataSource(self.treemap_data))
        series = [{'data': [{'color': '#7cb5ec', 'value': 6, 'id': 'id_00', 'parent': 'id_0', 'name': 'Road Accident'}, {'color': '#7cb5ec', 'value': 9, 'id': 'id_01', 'parent': 'id_0', 'name': 'Cardiovascular Disease'}, {'color': '#7cb5ec', 'id': 'id_0', 'value': 15, 'name': 'China'}, {'color': '#434348', 'value': 5, 'id': 'id_12', 'parent': 'id_1', 'name': 'Road Accident'}, {'color': '#434348', 'value': 10, 'id': 'id_13', 'parent': 'id_1', 'name': 'Cardiovascular Disease'}, {'color': '#434348', 'id': 'id_1', 'value': 15, 'name': 'India'}]}]
        self.assertEqual(chart.get_series(), series)

    # Modifiy after color functionality is there in TreeMap
    def test_get_series_with_colors(self):
        pass


class TestHighchartsPieDonut(TestHighchartsPieChart):
    chart_klass = highcharts.PieDonut
    pie_data = [["Country", "Cause", "Death Rate"],
                    ["India", "Cardiovascular Disease", 10],
                    ["India", "Road Accident", 5],
                    ["China", "Cardiovascular Disease", 9],
                    ["China", "Road Accident", 6]]

    def test_get_series(self):
        chart = self.chart_klass(data_source=SimpleDataSource(self.pie_data))
        series = [{'showInLegend': True, 'dataLabels': {'enabled': False}, 'data': [{'color': '#7cb5ec', 'y': 15, 'name': 'China'}, {'color': '#434348', 'y': 15, 'name': 'India'}], 'name': 'Country', 'size': '60%'}, {'innerSize': '60%', 'data': [{'color': '#7cb5ec', 'y': 6, 'name': 'Road Accident'}, {'color': '#7cb5ec', 'y': 9, 'name': 'Cardiovascular Disease'}, {'color': '#434348', 'y': 5, 'name': 'Road Accident'}, {'color': '#434348', 'y': 10, 'name': 'Cardiovascular Disease'}], 'name': 'Cause', 'size': '80%'}]
        self.assertEqual(chart.get_series(), series)

    # To be modified once color functionality is added to Chart.
    def test_get_series_with_colors(self):
        pass


class TestHighchartsHighMap(TestBaseHighcharts):
    chart_klass = highcharts.HighMap

    map_data_us_multi_series_lat_lon = [
        ['Latitude', 'Longitude', 'Winner', 'Seats'],
        [32.380120, -86.300629, 'Trump', 10],
        [58.299740, -134.406794, 'Trump', 10]]
    map_data_us_multi_series = [
        ['State', 'Winner', 'Seats'],
        ['us-nj', 'Trump', 10],
        ['us-ri', 'Trump', 10]]
    map_data_us_lat_lon = [
        ['Latitude', 'Longitude', 'Population'],
        [32.380120, -86.300629, 900],
        [58.299740, -134.406794, 387],
        [33.448260, -112.075774, 313],
    ]
    map_data_us = [
        ['State', 'Population'],
        ['us-nj', 438],
        ['us-ri', 387]]
    map_data_us_point = [
        ['Lat', 'Lon', 'Name', 'Date'],
        [46.8797, -110.3626, 'trump', '25th February'],
        [41.4925, -99.9018, 'trump', '26th February'],
        [45.4925, -89.9018, 'trump', '27th February']]

    def test_highmap_chart(self):
        chart = self.chart_klass(data_source=SimpleDataSource(self.map_data_us))
        self.assertEqual(chart.get_chart(), {'type': 'map'})
        self.assertNotEqual(chart.as_html(), "")
        chart = self.chart_klass(data_source=SimpleDataSource(self.map_data_us_lat_lon))
        self.assertEqual(chart.get_chart(), {'type': 'mapbubble'})

    def test_get_series(self):
        chart = self.chart_klass(data_source=SimpleDataSource(self.map_data_us))
        series = [{'joinBy': ['hc-key', 'code'], 'data': [{'code': 'us-nj', 'value': 438}, {'code': 'us-ri', 'value': 387}], 'name': 'Population'}]
        self.assertEqual(chart.get_series(), series)
        chart = self.chart_klass(data_source=SimpleDataSource(self.map_data_us_point))
        series = [{'color': 'black', 'type': 'map', 'name': 'Regions', 'showInLegend': False}, {'joinBy': ['hc-key', 'code'], 'data': [{'lat': 46.8797, 'Date': '25th February', 'lon': -110.3626}, {'lat': 41.4925, 'Date': '26th February', 'lon': -99.9018}, {'lat': 45.4925, 'Date': '27th February', 'lon': -89.9018}], 'name': 'trump'}]
        self.assertEqual(chart.get_series(), series)
        chart = self.chart_klass(data_source=SimpleDataSource(self.map_data_us_lat_lon))
        series = [{'type': 'map', 'name': 'Basemap', 'showInLegend': False}, {'joinBy': ['hc-key', 'code'], 'data': [{'lat': 32.38012, 'z': 900, 'lon': -86.300629}, {'lat': 58.29974, 'z': 387, 'lon': -134.406794}, {'lat': 33.44826, 'z': 313, 'lon': -112.075774}], 'name': 'Population'}]
        self.assertEqual(chart.get_series(), series)
        chart = self.chart_klass(data_source=SimpleDataSource(self.map_data_us_multi_series))
        series = [{'joinBy': ['hc-key', 'code'], 'data': [{'code': 'us-nj', 'Seats': 10}, {'code': 'us-ri', 'Seats': 10}], 'name': 'Trump'}]
        self.assertEqual(chart.get_series(), series)
        chart = self.chart_klass(data_source=SimpleDataSource(self.map_data_us_multi_series_lat_lon))
        series = [{'color': 'black', 'type': 'map', 'name': 'Regions', 'showInLegend': False}, {'joinBy': ['hc-key', 'code'], 'data': [{'lat': 32.38012, 'lon': -86.300629, 'Seats': 10}, {'lat': 58.29974, 'lon': -134.406794, 'Seats': 10}], 'name': 'Trump'}]
        self.assertEqual(chart.get_series(), series)

    # Needs some modification
    def test_get_series_with_colors(self):
        pass

    def test_get_color_axis(self):
        chart = self.chart_klass(data_source=self.data_source)
        self.assertEqual(chart.get_color_axis(), {})

    # What should be done for this ? Should it be kept or removed ?
    def test_get_map(self):
        pass

    def test_get_yaxis_single_series(self):
        pass


class TestHighchartsDonutChart(TestHighchartsPieChart):
    chart_klass = highcharts.DonutChart

    def test_pie_chart(self):
        chart = self.chart_klass(data_source=self.data_source)
        self.assertEqual(chart.get_chart(), {'options3d': {'alpha': 45, 'enabled': True}, 'type': 'pie'})
        self.assertNotEqual(chart.as_html(), "")


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
