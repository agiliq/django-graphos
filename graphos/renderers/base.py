import random
import string
import json

from django.template.loader import render_to_string


random_letter = lambda: random.choice(string.ascii_letters)


class BaseChart(object):
    def __init__(self, data_source, html_id=None,
                 options={}, *args, **kwargs):
        self.data_source = data_source
        self.html_id = html_id or "".join([random_letter()
                                          for el in range(10)])

    def get_data_json(self):
        return json.dumps(self.get_data())

    def get_data(self):
        return self.data_source.get_data()

    def get_html_id(self):
        return self.html_id

    def as_html(self):
        context = {"data": self.get_data(), "chart": self}
        return render_to_string(self.get_template(), context)
