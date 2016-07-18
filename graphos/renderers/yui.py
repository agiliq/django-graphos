from .base import BaseChart


class BaseYuiChart(BaseChart):
    def get_data(self):
        data = super(BaseYuiChart, self).get_data()
        header = self.header
        data_only = data[1:]
        rows = []
        for row in data_only:
            rows.append(dict(zip(header, row)))
        return rows

    def get_category_key(self):
        return self.data_source.get_header()[0]

    def get_html_template(self):
        return "graphos/yui/html.html"


class LineChart(BaseYuiChart):
    def get_js_template(self):
        return "graphos/yui/line_chart.html"


class BarChart(BaseYuiChart):
    def get_js_template(self):
        return "graphos/yui/bar_chart.html"


class ColumnChart(BaseYuiChart):
    def get_js_template(self):
        return "graphos/yui/column_chart.html"


class PieChart(BaseYuiChart):
    def get_js_template(self):
        return "graphos/yui/pie_chart.html"
