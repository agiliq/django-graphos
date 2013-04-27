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
