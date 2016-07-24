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

    def get_chart_type(self):
        return "line"


class SplineChart(BaseYuiChart):
    def get_js_template(self):
        return "graphos/yui/spline_chart.html"

    def get_chart_type(self):
        return "spline"


class BarChart(BaseYuiChart):
    def get_js_template(self):
        return "graphos/yui/bar_chart.html"

    def get_chart_type(self):
        return "bar"


class ColumnChart(BaseYuiChart):
    def get_js_template(self):
        return "graphos/yui/column_chart.html"

    def get_chart_type(self):
        return "column"


class PieChart(BaseYuiChart):
    def get_js_template(self):
        return "graphos/yui/pie_chart.html"

    def get_chart_type(self):
        return "pie"


class AreaChart(BaseYuiChart):
    def get_js_template(self):
        return "graphos/yui/area_chart.html"

    def get_chart_type(self):
        return "area"


class AreaSplineChart(BaseYuiChart):
    def get_js_template(self):
        return "graphos/yui/area_spline_chart.html"

    def get_chart_type(self):
        return "areaspline"
