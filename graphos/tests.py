from django.test import TestCase
from graphos.templatetags.graphos_tags import plot_model_series
from graphos.templatetags.graphos_tags import plot_redis_series

from .sources.base import BaseDataSource
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
