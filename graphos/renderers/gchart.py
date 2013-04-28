from .base import BaseChart

from django.template.loader import render_to_string


class LineChart(BaseChart):
    def get_template(self):
        return "graphos/gchart/line_chart.html"


class ColumnChart(BaseChart):
    def get_template(self):
        return "graphos/gchart/column_chart.html"


class BarChart(BaseChart):
    def get_template(self):
        return "graphos/gchart/bar_chart.html"


class CandlestickChart(BaseChart):
    def get_template(self):
        return "graphos/gchart/candlestick_chart.html"

