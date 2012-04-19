"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from graphos.templatetags.graphos_tags import plot_model_series
from graphos.templatetags.graphos_tags import plot_redis_series


class TagTest(TestCase):
    def test_model_all_options(self):
        """
        Tests template generation for the graphos library tags for plotting models
        """
        model_html = plot_model_series('1', 'core', 'value', count=200, y_max=200, frequency=500, \
                                width=600, height=300, color='#F33')
        self.assertIn('core/value/200', model_html, "Test Failed !!! URL not generated correctly")

    def test_model_min_options(self):
        """
        Tests template generation for the graphos library tags for plotting models
        """
        model_html = plot_model_series('1', 'core', 'value')
        self.assertIn('core/value/100', model_html, "Minimum argument response not met")

    def test_redis_all_options(self):
        """
        Tests template generation for the graphos library tags for plotting redis lists
        """
        redis_html = plot_redis_series('1', 'seashell', 'graphos', count=300, y_max=100, \
                        frequency=500, width=600, height=300, color='#F33')
        self.assertIn('seashell/graphos/300', redis_html, "Test Failed !!! \
                                    URL not generated correctly")
        redis_html = plot_redis_series('1', 'seashell', 'graphos', count=400, y_max=400, \
                        frequency=500, width=600, height=300, color='#F33')
        self.assertNotIn('seashell/graphos/100', redis_html, "Test Failed !!! \
                                    URL not generated correctly")

    def test_redis_min_options(self):
        """
        Tests template generation for the graphos library tags for plotting redis lists
        """
        redis_html = plot_redis_series('1', 'seashell', 'graphos')
        self.assertIn('seashell/graphos/100', redis_html, "Minimum argument response not correct")
