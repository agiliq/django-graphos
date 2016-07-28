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
    
    def get_data(self):
        # FIXME
        data = self.data_source.get_data()
        header = self.header
        header_first_two_columns = header[:2]
        data_only = data[1:]
        data_only_with_first_two_columns = [each[:2] for each in data_only]
        rows = []
        for row in data_only_with_first_two_columns:
            rows.append(dict(zip(header_first_two_columns, row)))
        return rows


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


class ComboChart(BaseYuiChart):
    def get_js_template(self):
        return "graphos/yui/combo.html"

    def get_chart_type(self):
        return "combo"


class ComboSplineChart(BaseYuiChart):
    def get_js_template(self):
        return "graphos/yui/combo_spline.html"

    def get_chart_type(self):
        return "combospline"


class MarkerSeriesChart(BaseYuiChart):
    def get_js_template(self):
        return "graphos/yui/marker_series.html"

    def get_chart_type(self):
        return "markerseries"