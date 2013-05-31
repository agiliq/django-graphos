from django.test import TestCase
from django.test import Client

from django.core.urlresolvers import reverse


class SimpleTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_homepage(self):
        self.client.get(reverse("demo_home"))

    def test_tutorial(self):
        self.client.get(reverse("demo_tutorial"))

    def test_gchart_demo(self):
        self.client.get(reverse("demo_gchart_demo"))

    def test_demo_yui_demo(self):
        self.client.get(reverse("demo_gchart_demo"))

    def test_demo_flot_demo(self):
        self.client.get(reverse('demo_flot_demo'))

    def test_demo_morris_demo(self):
        self.client.get(reverse('demo_morris_demo'))

    def test_demo_highcharts_demo(self):
        self.client.get(reverse('demo_highcharts_demo'))


    def test_demo_time_series_example(self):
        self.client.get(reverse('demo_time_series_example'))
