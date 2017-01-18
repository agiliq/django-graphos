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
        options = self.get_options()
        for i, name in enumerate(series_names):
            series = {"name": name, "data": column(data, i+1)[1:]}
            # If colors was passed then add color for the serieses
            if 'colors' in options and len(options['colors']) > i:
                series['color'] = options['colors'][i]
            serieses.append(series)
        serieses = self.add_series_options(serieses)
        return serieses

    def add_series_options(self, serieses):
        # hookpoint. You can subclass BaseHighCharts or its subclasses
        # and override this method to modify serieses.
        # eg: If you want to add dashStyle for a particular series of serieses
        # See http://api.highcharts.com/highcharts/ for options that can be added for series
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

    def get_title(self):
        title = self.get_options().get('title', {})
        if type(title) == str:
            title = {'text': title}
        return title

    def get_title_json(self):
        title = self.get_title()
        return json.dumps(title, cls=JSONEncoderForHTML)

    def get_subtitle(self):
        subtitle = self.get_options().get('subtitle', {})
        if type(subtitle) == str:
            subtitle = {'text': subtitle}
        return subtitle

    def get_subtitle_json(self):
        subtitle = self.get_subtitle()
        return json.dumps(subtitle, cls=JSONEncoderForHTML)

    def get_chart(self):
        chart = self.get_options().get('chart', {})
        chart['type'] = self.get_chart_type()
        return chart

    def get_chart_json(self):
        chart = self.get_chart()
        return json.dumps(chart, cls=JSONEncoderForHTML)

    def get_x_axis(self):
        x_axis = self.get_options().get('xAxis', {})
        if not 'categories' in x_axis:
            x_axis['categories'] = self.get_categories()
        if not 'title' in x_axis:
            x_axis['title'] = {}
        if not 'text' in x_axis['title']:
            x_axis['title']['text'] = self.get_x_axis_title()
        return x_axis

    def get_x_axis_json(self):
        x_axis = self.get_x_axis()
        return json.dumps(x_axis, cls=JSONEncoderForHTML)

    def get_y_axis(self):
        y_axis = self.get_options().get('yAxis', {})
        return y_axis

    def get_y_axis_json(self):
        y_axis = self.get_y_axis()
        return json.dumps(y_axis, cls=JSONEncoderForHTML)

    def get_tooltip(self):
        tooltip = self.get_options().get('tooltip', {})
        return tooltip

    def get_tooltip_json(self):
        tooltip = self.get_tooltip()
        return json.dumps(tooltip, cls=JSONEncoderForHTML)

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

    def get_series(self):
        # Currently graphos highmap only work with two columns, essentially that means only one series
        # That's why you see kv[1] and nothing beyond kv[1]
        # Can highcharts maps make sense for multiple serieses?
        data = self.get_data()[1:]
        first_series = {}
        options = self.get_options()
        first_series['data'] = []
        for i, kv in enumerate(data):
            region_detail = {'code': kv[0], 'value': kv[1]}
            first_series['data'].append(region_detail)
        # TODO: Make joinBy configurable. It could be something different from hc-key
        first_series['joinBy'] = ['hc-key', 'code']
        first_series['name'] = self.get_series_name()
        serieses = []
        serieses.append(first_series)
        return serieses

    def get_js_template(self):
        return "graphos/highcharts/js_highmaps.html"

    def get_map(self):
        # return "custom/world"
        # return "countries/us/custom/us-all-territories"
        return self.get_options().get('map_area', 'custom/world')

    def get_series_name(self):
        return self.get_data()[0][1]

    def get_color_axis(self):
        color_axis = self.get_options().get('colorAxis', {})
        return color_axis

    def get_color_axis_json(self):
        color_axis = self.get_color_axis()
        return json.dumps(color_axis, cls=JSONEncoderForHTML)

    def get_plot_options(self):
        plot_options = self.get_options().get('plotOptions', {})
        if not 'map' in plot_options:
            plot_options['map'] = {}
        return plot_options

    def get_plot_options_json(self):
        plot_options = self.get_plot_options()
        return json.dumps(plot_options, cls=JSONEncoderForHTML)


def column(matrix, i):
    return [row[i] for row in matrix]


def pie_column(matrix, i):
    return [{'name':row[0],'y':row[1]} for row in matrix]
