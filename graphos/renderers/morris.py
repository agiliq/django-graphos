from .base import BaseChart
import json

from ..utils import JSONEncoderForHTML

class BaseMorrisChart(BaseChart):

    def get_data(self):
        header = self.header
        data = super(BaseMorrisChart, self).get_data()
        data_only = data[1:]
        rows = []
        for row in data_only:
            rows.append(dict(zip(header, row)))
        return rows

    def get_category_key(self):
        return self.header[0]

    def get_y_keys(self):
        try:
            return json.dumps(self.options['ykeys'], cls=JSONEncoderForHTML)
        except KeyError:
            return json.dumps(self.header[1:], cls=JSONEncoderForHTML)

    def get_html_template(self):
        return "graphos/morris/html.html"

    def get_js_template(self):
        return "graphos/morris/chart.html"


class LineChart(BaseMorrisChart):
    def chart_type(self):
        return "Line"


class BarChart(BaseMorrisChart):
    def chart_type(self):
        return "Bar"


class DonutChart(BaseMorrisChart):
    def get_data(self):
        data = super(BaseMorrisChart, self).get_data()
        data_only = data[1:]
        return [{"label": el[0], "value": el[1]} for el in data_only]

    def chart_type(self):
        return "Donut"

    def get_js_template(self):
        return "graphos/morris/donut_chart.html"


class AreaChart(BaseMorrisChart):
    def chart_type(self):
        return "Area"
