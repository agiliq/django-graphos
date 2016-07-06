from .base import BaseChart
import json

from django.template.loader import render_to_string
from ..utils import JSONEncoderForHTML


class BaseHighCharts(BaseChart):
    def get_html_template(self):
        return "graphos/highcharts/html.html"

    def get_js_template(self):
        return "graphos/highcharts/js.html"

    def get_series(self):
        data = self.get_data()
        series_names = data[0][1:]
        serieses = []
        for i, name in enumerate(series_names):
            serieses.append({"name": name, "data": column(data, i+1)[1:]})
        return self.data_source.to_json(serieses)

    def get_categories(self):
        return self.data_source.to_json(column(self.get_data(), 0)[1:])

    def get_x_axis_title(self):
        return self.get_data()[0][0]


class LineChart(BaseHighCharts):
    def get_chart_type(self):
        return "line"


class BarChart(BaseHighCharts):
    def get_chart_type(self):
        return "bar"


class ColumnChart(BaseHighCharts):
    def get_chart_type(self):
        return "column"


class PieChart(BaseHighCharts):
    def get_chart_type(self):
        return "pie"


def column(matrix, i):
    return [row[i] for row in matrix]
