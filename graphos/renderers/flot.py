from .base import BaseChart
from ..utils import get_default_options


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
        return self.data_source.to_json(self.get_series_objects())

    def get_options(self):
        options = get_default_options()
        options.update(self.options)
        return options

    def get_template(self):
        return 'graphos/flot.html'


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
    pass  # TODO
