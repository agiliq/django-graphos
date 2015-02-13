from .base import BaseChart
import json

from django.template.loader import render_to_string
from ..utils import JSONEncoderForHTML

class BaseMorrisChart(BaseChart):
    def get_data_json(self):
        header = self.data_source.get_header()
        data_only = self.get_data()[1:]
        rows = []
        for row in data_only:
            rows.append(dict(zip(header, row)))

        return json.dumps(rows, cls=JSONEncoderForHTML)

    def get_category_key(self):
        return self.data_source.get_header()[0]

    def get_y_keys(self):
        return json.dumps(self.data_source.get_header()[1:], cls=JSONEncoderForHTML)


    def get_template(self):
        return "graphos/morris/chart.html"



class LineChart(BaseMorrisChart):
    def chart_type(self):
        return "Line"


class BarChart(BaseMorrisChart):
    def chart_type(self):
        return "Bar"

class DonutChart(BaseMorrisChart):
    def get_data_json(self):
        data_only = self.get_data()[1:]
        return json.dumps([{"label": el[0], "value": el[1]} for el in data_only], cls=JSONEncoderForHTML)

    def chart_type(self):
        return "Donut"

    def get_template(self):
        return "graphos/morris/donut_chart.html"
