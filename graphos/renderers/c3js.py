import json
from .base import BaseChart


class BaseC3JS(BaseChart):
    """docstring for BaseC3JS"""
    def get_data(self):
        return super(BaseC3JS, self).get_data()

    def get_html_template(self):
        return "graphos/c3js/html.html"

    def get_js_template(self):
        return "graphos/c3js/js.html"

    def get_categories(self):
        return [x[0] for x in self.get_data()]

    def get_x_axis_title(self):
        return self.get_data()[0][0]

    def get_columns_data(self):
        return json.dumps(map(list, zip(*self.get_data())))

    def get_pie_data(self):
        return json.dumps(self.get_data()[1:])


class LineChart(BaseC3JS):
    def get_chart_type(self):
        return "line"


class BarChart(BaseC3JS):
    def get_chart_type(self):
        return "bar"


class SplineChart(BaseC3JS):
    def get_chart_type(self):
        return "spline"


class PieChart(BaseC3JS):
    def get_chart_type(self):
        return "pie"


class ColumnChart(BaseC3JS):
    """
    C3 doesn't have column type chart, so we have to render the column chart by
    rotating the axis in the js
    axis: {
        rotated: true
    }
    """
    def get_chart_type(self):
        return "column"


class DonutChart(BaseC3JS):
    def get_chart_type(self):
        return "donut"
