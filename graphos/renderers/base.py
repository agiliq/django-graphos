import random
import string
import json

from django.template.loader import render_to_string


random_letter = lambda: random.choice(string.ascii_letters)

DEFAULT_HEIGHT = 400
DEFAULT_WIDTH = 800


class BaseChart(object):
    def __init__(self, data_source, html_id=None,
                 width=None, height=None,
                 options=None, *args, **kwargs):
        self.data_source = data_source
        self.html_id = html_id or "".join([random_letter()
                                          for el in range(10)])

        self.height = height or DEFAULT_HEIGHT
        self.width = width or DEFAULT_WIDTH
        self.options = options or {}
        self.header = data_source.get_header()

    def get_data(self):
        return self.data_source.get_data()

    def get_data_json(self):
        return json.dumps(self.get_data())

    def get_options(self):
        options = self.options
        if not 'title' in options:
            options['title'] = "Chart"
        return options

    def get_options_json(self):
        return json.dumps(self.get_options())

    def get_html_id(self):
        return self.html_id

    def get_template(self):
        return 'charts/base_chart.html'

    def as_html(self):
        context = {"chart": self}
        return render_to_string(self.get_template(), context)
