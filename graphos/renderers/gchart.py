from .base import BaseChart


class BaseGChart(BaseChart):
    def get_html_template(self):
        return "graphos/gchart/html.html"


class LineChart(BaseGChart):
    def get_js_template(self):
        return "graphos/gchart/line_chart.html"


class GaugeChart(BaseGChart):
    def get_js_template(self):
        return "graphos/gchart/gauge_chart.html"


class ColumnChart(BaseGChart):
    def get_js_template(self):
        return "graphos/gchart/column_chart.html"


class BarChart(BaseGChart):
    def get_js_template(self):
        return "graphos/gchart/bar_chart.html"

    def get_options(self):
        options = super(BarChart, self).get_options()
        if not 'vAxis' in options:
            vaxis = self.data_source.get_header()[0]
            options['vAxis'] = {'title': vaxis}
        return options


class CandlestickChart(BaseGChart):
    def get_js_template(self):
        return "graphos/gchart/candlestick_chart.html"


class PieChart(BaseGChart):
    def get_js_template(self):
        return "graphos/gchart/pie_chart.html"


class TreeMapChart(BaseGChart):
    def get_js_template(self):
        return "graphos/gchart/treemap_chart.html"


class AreaChart(BaseGChart):
    def get_js_template(self):
        return "graphos/gchart/area_chart.html"
