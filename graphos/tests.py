from django.test import TestCase
from graphos.templatetags.graphos_tags import plot_model_series
from graphos.templatetags.graphos_tags import plot_redis_series

from .sources.base import BaseDataSource


class TestSources(TestCase):
    def test_base_data_source(self):
        data_source = BaseDataSource()
        self.assertTrue(hasattr(data_source, "get_data"))
        self.assertRaises(Exception, data_source.get_data,)
