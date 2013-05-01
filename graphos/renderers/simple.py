from .base import BaseChart


class SimpleChart(BaseChart):
    def get_template(self):
        return 'graphos/simple_chart.html'
