from .base import BaseChart
from django.template.loader import render_to_string

import json
from ..utils import JSONEncoderForHTML


class BaseYuiChart(BaseChart):
    def get_data_json(self):
        header = self.data_source.get_header()
        data_only = self.get_data()[1:]
        rows = []
        for row in data_only:
            rows.append(dict(zip(header, row)))

        return json.dumps(rows, cls=JSONEncoderForHTML)

    def get_category_key(self):
        return self.data_source.get_header()[0]


class LineChart(BaseYuiChart):
    def get_template(self):
        return "graphos/yui/line_chart.html"


class BarChart(BaseYuiChart):
    def get_template(self):
        return "graphos/yui/bar_chart.html"


class ColumnChart(BaseYuiChart):
    def get_template(self):
        return "graphos/yui/column_chart.html"

class PieChart(BaseYuiChart):
    def get_template(self):
        return "graphos/yui/pie_chart.html"
