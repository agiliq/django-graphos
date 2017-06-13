from .base import BaseChart

import json


class BaseChartJs(BaseChart):
    def get_data(self):
        data = super(BaseChartJs, self).get_data()
        data_only = data[1:]
        context = []
        for row in data_only:
            context_dict = {}
            context_dict['label'] = row[0]
            context_dict['data'] = row[1:]
            context_dict['backgroundColor'] = 'rgba(75,192,192,1)'
            context.append(context_dict)
        if self.get_options():
            context[0].update(self.get_options())
        return json.dumps(context)

    def get_html_template(self):
        return "graphos/chartjs/html.html"

    def get_js_template(self):
        return "graphos/chartjs/js.html"


class LineChart(BaseChartJs):
    def get_chart_type(self):
        return "line"


class BarChart(BaseChartJs):
    def get_chart_type(self):
        return "bar"


class PieChart(BaseChartJs):
    def get_chart_type(self):
        return "pie"


class DoughnutChart(BaseChartJs):
    def get_chart_type(self):
        return "doughnut"