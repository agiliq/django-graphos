from django.test import TestCase
from graphos.templatetags.graphos_tags import plot_model_series
from graphos.templatetags.graphos_tags import plot_redis_series

from .sources.base import BaseDataSource
from .sources.simple import SimpleDataSource
from .exceptions import GraphosException


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
