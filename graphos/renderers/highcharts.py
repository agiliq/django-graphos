from .base import BaseChart
import json

from django.template.loader import render_to_string
from ..utils import JSONEncoderForHTML


class BaseHighCharts(BaseChart):
    def get_html_template(self):
        return "graphos/highcharts/html.html"

    def get_js_template(self):
        return "graphos/highcharts/js.html"

    def get_series(self):
        """
        Example usage:
            data = [
               ['Year', 'Sales', 'Expenses', 'Items Sold', 'Net Profit'],
               ['2004', 1000, 400, 100, 600],
               ['2005', 1170, 460, 120, 310],
               ['2006', 660, 1120, 50, -460],
               ['2007', 1030, 540, 100, 200],
            ]
            sd = SimpleDataSource(data)
            hc = BaseHighCharts(sd)
            hc.get_series() would be [{"name": "Sales", "data": [1000, 1170, 660, 1030]}, {"name": "Expenses", "data": [400, 460, 1120, 540]} ....]
        """
        data = self.get_data()
        series_names = data[0][1:]
        serieses = []
        for i, name in enumerate(series_names):
            serieses.append({"name": name, "data": column(data, i+1)[1:]})
        return serieses

    def get_series_json(self):
        serieses = self.get_series()
        return json.dumps(serieses, cls=JSONEncoderForHTML)

    def get_categories(self):
        """
        This would return [2004, 2005, 2006, 2007]
        """
        return column(self.get_data(), 0)[1:]

    def get_categories_json(self):
        categories = self.get_categories()
        return json.dumps(categories, cls=JSONEncoderForHTML)

    def get_x_axis_title(self):
        return self.get_data()[0][0]


class LineChart(BaseHighCharts):
    def get_chart_type(self):
        return "line"


class BarChart(BaseHighCharts):
    def get_chart_type(self):
        return "bar"


class ColumnChart(BaseHighCharts):
    def get_chart_type(self):
        return "column"


class ColumnLineChart(BaseHighCharts):
    """
    First series will be plotted as column
    Every subsequent series will be plotted as line
    """

    def get_series(self):
        data = self.get_data()
        serieses = []
        serieses.append({"name": data[0][1], "data": column(data, 1)[1:], "type": "column"})
        series_names = data[0][2:]
        for i, name in enumerate(series_names):
            serieses.append({"name": name, "data": column(data, i+2)[1:], "type": "line"})
        return serieses


class LineColumnChart(BaseHighCharts):
    """
    First series will be plotted as line
    Every subsequent series will be plotted as column
    """

    def get_series(self):
        data = self.get_data()
        serieses = []
        serieses.append({"name": data[0][1], "data": column(data, 1)[1:], "type": "line"})
        series_names = data[0][2:]
        for i, name in enumerate(series_names):
            serieses.append({"name": name, "data": column(data, i+2)[1:], "type": "column"})
        return serieses


class PieChart(BaseHighCharts):
    def get_series(self):
        data = self.get_data()
        series_names = data[0][1:]
        serieses = []
        for i, name in enumerate(series_names):
            serieses.append({"name": name, "data": pie_column(data, i+1)[1:]})
        return serieses

    def get_chart_type(self):
        return "pie"


class AreaChart(BaseHighCharts):
    def get_chart_type(self):
        return "area"


class DonutChart(BaseHighCharts):
    def get_series(self):
        _data = super(DonutChart, self).get_data()
        return _data[1:]

    def get_series_name(self):
        return self.get_data()[0][1]

    def get_js_template(self):
        return "graphos/highcharts/js_donut.html"

    def get_chart_type(self):
        return "pie"


class ScatterChart(BaseHighCharts):
    def get_chart_type(self):
        return "scatter"


class LogarithmicChart(BaseHighCharts):
    def get_series(self):
        data = super(LogarithmicChart, self).get_series()
        data = data[0].get('data')
        return data

    def get_js_template(self):
        return "graphos/highcharts/js_log.html"

    def get_chart_type(self):
        return "log_chart"


class MultiAxisChart(BaseHighCharts):
    def get_series(self):
        data = super(MultiAxisChart, self).get_series()
        return [x.get('data') for x in data]

    def get_y_axis_titles(self):
        data = super(MultiAxisChart, self).get_series()
        return [x.get('name') for x in data]

    def get_js_template(self):
        return "graphos/highcharts/js_dual_axis.html"

    def get_chart_type(self):
        return "multi_axis"


class HighMap(BaseHighCharts):
    """docstring for HighMaps"""
    def __init__(self, *args, **kwargs):
        super(HighMap, self).__init__(*args, **kwargs)
        self.options['series_name'] = self.get_data()[0][1]

    def get_series(self):
        data = self.get_data()[1:]
        final_data = []
        for kv in data:
            final_data.append({'code': kv[0], 'value': kv[1]})
        return final_data

    def get_chart_type(self):
        return "map_chart"

    def get_js_template(self):
        return "graphos/highcharts/js_highmaps.html"

    def get_map(self):
        # return "custom/world"
        # return "countries/us/custom/us-all-territories"
        return self.get_options().get('map_area', 'custom/world')

    def get_series_name(self):
        return self.get_options().get('series_name', 'Value')


def column(matrix, i):
    return [row[i] for row in matrix]


def pie_column(matrix, i):
    return [{'name':row[0],'y':row[1]} for row in matrix]
