from django.test import TestCase
from graphos.templatetags.graphos_tags import plot_model_series
from graphos.templatetags.graphos_tags import plot_redis_series

from .sources.base import BaseDataSource
from .sources.simple import SimpleDataSource
from .sources.csv_file import CSVDataSource
from .sources.model import ModelDataSource

from .renderers.flot import LineChart
from .exceptions import GraphosException

from demo.models import Account

import os
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


class TestRenderers(TestCase):
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
        chart = LineChart(data_source=self.data_source)
        json_data = chart.get_serieses()
        series_1 = [(2004, 1000), (2005, 1170), (2006, 660), (2007, 1030)]
        series_2 = [(2004, 400), (2005, 460), (2006, 1120), (2007, 540)]
        self.assertEqual([series_1, series_2], json_data)
