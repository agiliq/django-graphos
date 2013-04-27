import json
import random
import string

from .base import BaseChart

from django.template.loader import render_to_string


class LineChart(BaseChart):
    """ LineChart """

    def __init__(self, *args, **kwargs):
        super(LineChart, self).__init__(*args, **kwargs)

    def get_serieses(self):
        data_only = self.get_data()[1:]
        first_column = [el[0] for el in data_only]
        serieses = []
        for i in range(1, len(self.header)):
            current_column = [el[i] for el in data_only]
            current_series = zip(first_column, current_column)
            serieses.append(current_series)
        return serieses

    def get_series_objects(self):
        series_objects = []
        serieses = self.get_serieses()
        for i in range(1, len(self.header)):
            series_object = {}
            series_object['label'] = self.header[i]
            series_object['data'] = serieses[i-1]
            series_objects.append(series_object)
        return series_objects

    def get_series_objects_json(self):
        return json.dumps(self.get_series_objects())

    def get_template(self):
        template = 'charts/line_chart.html'
        return template

    def as_html(self):
        series = self.get_series_objects_json()
        options = self.get_options_json()
        context = { 'series': series, 'html_id': self.html_id, 'options': options}
        return render_to_string(self.get_template(), context)
