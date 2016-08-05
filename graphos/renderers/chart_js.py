from .base import BaseChart


class BaseCJsChart(BaseChart):
    def get_data(self):
        data = super(BaseCJsChart, self).get_data()
        data_only = data[1:]
        context = []
        for row in data_only:
            context_dict = {}
            context_dict['label'] = row[0]
            context_dict['data'] = row[1:]
            context_dict['backgroundColor'] = 'rgba(75,192,192,1)'
            context.append(context_dict)
        return context

    def get_html_template(self):
        return "graphos/chart_js/html.html"


class LineChart(BaseCJsChart):
    def get_js_template(self):
        return "graphos/chart_js/line_chart.html"

    def get_chart_type(self):
        return "line"