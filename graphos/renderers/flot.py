import json

from .base import BaseChart
from ..utils import get_default_options, JSONEncoderForHTML


class BaseFlotChart(BaseChart):
    """ LineChart """

    def get_serieses(self):
        # Assuming self.data_source.data is:
        # [['Year', 'Sales', 'Expenses'], [2004, 100, 200], [2005, 300, 250]]
        data_only = self.get_data()[1:]
        # first_column = [2004, 2005]
        first_column = [el[0] for el in data_only]
        serieses = []
        for i in range(1, len(self.header)):
            current_column = [el[i] for el in data_only]
            current_series = self.zip_list(first_column, current_column)
            serieses.append(current_series)
        # serieses = [[(2004, 100), (2005, 300)], [(2004, 200), (2005, 250)]]
        return serieses

    def get_series_objects(self):
        series_objects = []
        serieses = self.get_serieses()
        for i in range(1, len(self.header)):
            series_object = {}
            series_object['label'] = self.header[i]
            series_object['data'] = serieses[i - 1]
            series_objects.append(series_object)
        # series_objects = [{'label': 'Sales', 'data': [(2004, 100), (2005, 300)]}, {'label': 'Expenses': 'data': [(2004, 100), (2005, 300)]}]
        return series_objects

    def get_series_pie_objects(self):
        series_objects = []
        serieses = self.get_data()[1:]
        try:
            for i in serieses:
                series_object = {}
                series_object['label'] = i[0]
                series_object['data'] = i[1]
                series_objects.append(series_object)
        except IndexError:
            print("Input Data Format is [['Year', 'Sales'], [2004, 100], [2005, 300]]")
        # series_objects = [{'label': '2004', 'data': 100}, {'label': '2005': 'data': 300}]
        return json.dumps(series_objects, cls=JSONEncoderForHTML)

    def get_series_objects_json(self):
        return json.dumps(self.get_series_objects(), cls=JSONEncoderForHTML)

    def get_options(self):
        options = get_default_options()
        options.update(self.options)
        return options

    def get_html_template(self):
        return 'graphos/flot/html.html'

    def get_js_template(self):
        return 'graphos/flot/js.html'


class PointChart(BaseFlotChart):

    def get_options(self):
        options = get_default_options("points")
        options.update(self.options)
        return options


class LineChart(BaseFlotChart):
    """ LineChart """

    def get_options(self):
        options = get_default_options("lines")
        options.update(self.options)
        return options


class BarChart(BaseFlotChart):

    def get_options(self):
        options = get_default_options("bars")
        options.update(self.options)
        return options


class ColumnChart(BaseFlotChart):

    def get_options(self):
        options = get_default_options("bars")
        options.update(self.options)
        options["horizontal"] = True
        return options


class PieChart(BaseFlotChart):

    def get_options(self):
        options = get_default_options("pie")
        options.update(self.options)
        return options

    def get_js_template(self):
        return 'graphos/flot/pie_chart.html'
