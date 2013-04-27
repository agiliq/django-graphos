from .base import BaseChart

from django.template.loader import render_to_string


class LineChart(BaseChart):
    def get_template(self):
        return "graphos/gchart/line_chart.html"

class ColumnChart(BaseChart):
    def get_template(self):
        return "graphos/gchart/column_chart.html"

