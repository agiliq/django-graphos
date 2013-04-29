import json

from .base import BaseChart

from django.template.loader import render_to_string


def get_default_options():
    """ default options """
    legend = {"position": 'ne'}
    global_options = {"legend": legend}
    return global_options


class BaseFlotChart(BaseChart):
    """ LineChart """

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
            series_object['data'] = serieses[i - 1]
            series_objects.append(series_object)
        return series_objects

    def get_series_objects_json(self):
        return json.dumps(self.get_series_objects())

    def _get_options(self, type):
        series = {"%s" % type: {"show": "true"}}
        options = get_default_options()
        options.update({"series": series})
        context = super(BaseFlotChart, self).get_options()
        options.update(context)
        return options

    def get_template(self):
        template = 'charts/line_chart.html'
        return template

    def as_html(self):
        context = {'chart': self}
        return render_to_string(self.get_template(), context)


class PointChart(BaseFlotChart):

    def get_options(self):
        options = super(PointChart, self)._get_options("points")
        return options


class LineChart(BaseFlotChart):
    """ LineChart """

    def get_options(self):
        options = super(LineChart, self)._get_options("lines")
        return options


class BarChart(BaseFlotChart):

    def get_options(self):
        options = super(BarChart, self)._get_options("bars")
        return options
