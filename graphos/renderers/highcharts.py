from .base import BaseChart
import json
from collections import defaultdict
from decimal import Decimal

from django.template.loader import render_to_string
from ..utils import JSONEncoderForHTML
from ..exceptions import GraphosException


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

    def get_chart_type(self):
        raise GraphosException("Not Implemented")

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

    def get_credits(self):
        credits = self.get_options().get('credits', {})
        return credits

    def get_credits_json(self):
        credits = self.get_credits()
        return json.dumps(credits, cls=JSONEncoderForHTML)

    def get_exporting(self):
        exporting = self.get_options().get('exporting', {})
        return exporting

    def get_exporting_json(self):
        exporting = self.get_exporting()
        return json.dumps(exporting, cls=JSONEncoderForHTML)

    def get_legend(self):
        legend = self.get_options().get('legend', {})
        return legend

    def get_legend_json(self):
        legend = self.get_legend()
        return json.dumps(legend, cls=JSONEncoderForHTML)

    def get_navigation(self):
        navigation = self.get_options().get('navigation', {})
        return navigation

    def get_navigation_json(self):
        navigation = self.get_navigation()
        return json.dumps(navigation, cls=JSONEncoderForHTML)


class LineChart(BaseHighCharts):
    def get_chart_type(self):
        return "line"


class BarChart(BaseHighCharts):
    def get_chart_type(self):
        return "bar"


class ColumnChart(BaseHighCharts):
    def get_chart_type(self):
        return "column"


class AreaChart(BaseHighCharts):
    def get_chart_type(self):
        return "area"


class ScatterChart(BaseHighCharts):
    def get_chart_type(self):
        return "scatter"


class ColumnLineChart(BaseHighCharts):
    """
    First series will be plotted as column
    Every subsequent series will be plotted as line
    """

    def get_series(self):
        data = self.get_data()
        serieses = []
        # TODO: Add color ability
        serieses.append({"name": data[0][1], "data": column(data, 1)[1:], "type": "column"})
        series_names = data[0][2:]
        for i, name in enumerate(series_names):
            serieses.append({"name": name, "data": column(data, i+2)[1:], "type": "line"})
        return serieses

    def get_chart_type(self):
        # TODO: This is a placeholder so that get_chart() doesn't fail. Think how we can fix this.
        return "column_line"


class LineColumnChart(BaseHighCharts):
    """
    First series will be plotted as line
    Every subsequent series will be plotted as column
    """

    def get_series(self):
        data = self.get_data()
        serieses = []
        # TODO: Add color ability
        serieses.append({"name": data[0][1], "data": column(data, 1)[1:], "type": "line"})
        series_names = data[0][2:]
        for i, name in enumerate(series_names):
            serieses.append({"name": name, "data": column(data, i+2)[1:], "type": "column"})
        return serieses

    def get_chart_type(self):
        return "line_column"


class PieChart(BaseHighCharts):
    def get_series(self):
        data = self.get_data()
        series_names = data[0][1:]
        serieses = []
        for i, name in enumerate(series_names):
            # TODO: Add color ability
            series = {"name": name, "data": pie_column(data, i+1)[1:]}
            serieses.append(series)
        return serieses

    def get_chart_type(self):
        return "pie"


class DonutChart(PieChart):
    def get_js_template(self):
        return "graphos/highcharts/js_donut.html"

    def get_chart(self):
        chart = super(DonutChart, self).get_chart()
        chart['options3d'] = {'enabled': True, 'alpha': 45}
        return chart

    def get_plot_options(self):
        plot_options = self.get_options().get('plotOptions', {})
        plot_options['pie'] = {'innerSize': 100, 'depth': 45}
        return plot_options

    def get_plot_options_json(self):
        plot_options = self.get_plot_options()
        return json.dumps(plot_options, cls=JSONEncoderForHTML)


class MultiAxisChart(BaseHighCharts):
    # TODO: This should be renamed dual axis, its not multi axis
    # It will break with more than two serieses
    def get_series(self):
        serieses = super(MultiAxisChart, self).get_series()
        chart_types = ['column', 'spline']
        # Make series 0 as column and series 1 as line
        for i, series in enumerate(serieses):
            if i == 0:
                series['yAxis'] = 1
            series['type'] = chart_types[i]
        return serieses

    def get_y_axis(self):
        y_axis = super(MultiAxisChart, self).get_y_axis()
        # This is overriding any thing set in yAxis. Fix
        y_axis = []
        y_axis.append({'title': {'text': self.get_series()[1]['name']}})
        y_axis.append({'title': {'text': self.get_series()[0]['name']}, 'opposite': True})
        return y_axis

    def get_chart_type(self):
        return "multi_axis"


class HighMap(BaseHighCharts):
    """docstring for HighMaps"""
    def __init__(self, *args, **kwargs):
        super(HighMap, self).__init__(*args, **kwargs)
        self.is_lat_long = False
        first_column = self.get_data()[1][0]
        second_column = self.get_data()[1][1]
        if type(first_column) in [int, float, long, Decimal] and type(second_column) in [int, float, long, Decimal]:
            self.is_lat_long = True
        if not self.is_lat_long:
            value_to_check_for_series_type = self.get_data()[1][1]
        else:
            value_to_check_for_series_type = self.get_data()[1][2]
        if type(value_to_check_for_series_type) in [int, float, long, Decimal]: # TODO: It could be any numeric, not just int
            self.series_type = 'single_series'
        else:
            self.series_type = 'multi_series'

    def get_series(self):
        # Currently graphos highmap only work with two columns, essentially that means only one series
        # That's why you see kv[1] and nothing beyond kv[1]
        # Can highcharts maps make sense for multiple serieses?
        """
        Different serieses should come up based on different data formats passed.
            1. Single series
                This would be a choropleth map where the color intensity of different regions/polygons
                differ based on the integer values in series. Two things are important here
                    a: It works with a colorAxis
                    b: First series i.e second column of tabular data must be integer.
            2. Multiple series
                Example
                State     Winner    Seats
                Orissa    BJP       5
                Bihar     RJD       10
                Assam     BJP       7
                Meghalaya AAP       12
                Manipur   AAP       4
                Punjab    AAP       4

                In this case all states won by AAP make up one series and will be colored in a particular color.
                Then all states won by BJP will be colored in a particular color. This color will be different from AAP color.
                But colorAxis doesn't make sense here. It's not a choropleth map. But colorAxes(not colorAxis) could make senese here, i.e set color intensities for different serieses. But highcharts doesn't allow setting colorAxes, i.e color intensities for different serieses.
                Graphos internally finds out all the distinct entries of second column of tabular data and created different serieses for different states.
        """
        if self.series_type == 'single_series':
            serieses = self.calculate_single_series()
        else:
            serieses = self.calculate_multi_series()
        return serieses

    def calculate_multi_series(self):
        data = self.get_data()[1:]
        name_to_regions_dict = defaultdict(list)
        if not self.is_lat_long:
            second_column_onwards_names = self.get_data()[0][2:]
        else:
            second_column_onwards_names = self.get_data()[0][3:]
        chart_type = self.get_chart_type()
        for row in data:
            if not self.is_lat_long:
                series_name = row[1]
            else:
                series_name = row[2]
            # Create a dictionary of format {'code': 'Orissa', 'Seats': 5}
            if not self.is_lat_long:
                d = {'code': row[0]}
            else:
                d = {'lat': row[0], 'lon': row[1]}
            if not self.is_lat_long:
                second_column_onwards = row[2:]
            else:
                second_column_onwards = row[3:]
            second_column_onwards_dict = dict(zip(second_column_onwards_names, second_column_onwards))
            # If it is a mapbubble, add 'z' based on some key
            if chart_type == 'mapbubble':
                zKey = self.get_options().get('zKey')
                if zKey:
                    d['z'] = second_column_onwards_dict[zKey]
            d.update(second_column_onwards_dict)
            name_to_regions_dict[series_name].append(d)
        serieses = []
        join_by = self.get_options().get('joinBy', 'hc-key')
        i = 0
        colors = self.get_options().get('colors', None)
        for series_name, regions in name_to_regions_dict.items():
            series = {}
            series['name'] = series_name
            series['data'] = regions
            series['joinBy'] = [join_by, 'code']
            serieses.append(series)
            if colors and len(colors) > i:
                series['color'] = colors[i]
            i += 1
        if chart_type == 'mapbubble':
            just_for_sake_series = {}
            just_for_sake_series['name'] = 'Regions'
            just_for_sake_series['type'] = 'map'
            just_for_sake_series['color'] = 'black'
            just_for_sake_series['showInLegend'] = False
            serieses.insert(0, just_for_sake_series)
        return serieses

    def calculate_single_series(self):
        data = self.get_data()[1:]
        first_series = {}
        options = self.get_options()
        first_series['data'] = []
        chart_type = self.get_chart_type()
        for i, kv in enumerate(data):
            if chart_type == 'mapbubble':
                if not self.is_lat_long:
                    region_detail = {'code': kv[0], 'z': kv[1]}
                else:
                    region_detail = {'lat': kv[0], 'lon': kv[1], 'z': kv[2]}
            elif chart_type == 'map':
                region_detail = {'code': kv[0], 'value': kv[1]}
            first_series['data'].append(region_detail)
        join_by = self.get_options().get('joinBy', 'hc-key')
        first_series['joinBy'] = [join_by, 'code']
        first_series['name'] = self.get_series_name()
        serieses = []
        serieses.append(first_series)
        if chart_type == 'mapbubble':
            just_for_sake_series = {}
            just_for_sake_series['name'] = 'Basemap'
            just_for_sake_series['type'] = 'map'
            just_for_sake_series['showInLegend'] = False
            serieses.insert(0, just_for_sake_series)
        return serieses

    def get_js_template(self):
        return "graphos/highcharts/js_highmaps.html"

    def get_map(self):
        # return "custom/world"
        # return "countries/us/custom/us-all-territories"
        return self.get_options().get('map_area', 'custom/world')

    def get_series_name(self):
        if self.is_lat_long:
            return self.get_data()[0][2]
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
        if not 'mapbubble' in plot_options:
            plot_options['mapbubble'] = {}
        return plot_options

    def get_plot_options_json(self):
        plot_options = self.get_plot_options()
        return json.dumps(plot_options, cls=JSONEncoderForHTML)

    def get_chart_type(self):
        # If you are using mapbubble, ensure you don't set allAreas to False.
        # Also if you are setting mapbubble for a multi series chart, then probably you should set zKey too to get different bubble sizes.
        if self.is_lat_long:
            return "mapbubble"
        else:
            return self.get_options().get("map_type", "map")


def column(matrix, i):
    return [row[i] for row in matrix]


def pie_column(matrix, i):
    return [{'name':row[0],'y':row[i]} for row in matrix]



class HeatMap(BaseHighCharts):
    def remove_duplicates(self, lst):
        dset = set()
        # relies on the fact that dset.add() always returns None.
        return [l for l in lst if
                l not in dset and not dset.add(l)]

    def get_categories(self, columnID):
        # categories = super(HeatMap, self).get_categories()
        return self.remove_duplicates(column(self.get_data(), columnID))

    def get_series(self):
        data = self.get_data()[1:]
        serieses = []
        new_list = []
        X_list = self.remove_duplicates(column(data, 0))
        Y_list = self.remove_duplicates(column(data, 1))
        Value_list = column(data, 2)
        counter = 0
        for i in range(0,len(X_list)):
            for j in range(0, len(Y_list)):
                new_list.append([i, j, Value_list[counter]])
                counter += 1
        data = new_list
        serieses.append({"data": data})
        return serieses

    def get_x_axis(self):
        x_axis = []
        x_axis.append({'categories': self.get_categories(0)[1:],'title': {'enabled': True, 'text': self.get_categories(0)[0]}})
        return x_axis

    def get_y_axis(self):
        y_axis = []
        y_axis.append({'categories': self.get_categories(1)[1:],'title': {'enabled': True, 'text': self.get_categories(1)[0]}})
        return y_axis

    def get_color_axis(self):
        color_axis = self.get_options().get('colorAxis', {})
        return color_axis

    def get_color_axis_json(self):
        color_axis = self.get_color_axis()
        return json.dumps(color_axis, cls=JSONEncoderForHTML)

    def get_chart_type(self):
        return "heatmap"

    def get_js_template(self):
        return "graphos/highcharts/js_heatmaps.html"

    def get_plot_options(self):
        plot_options = self.get_options().get('plotOptions', {})
        if not 'heatmap' in plot_options:
            plot_options['heatmap'] = {}
        if 'borderWidth' not in plot_options['heatmap']:
            plot_options['heatmap']['borderWidth'] = 1
        if 'dataLabels' not in plot_options['heatmap']:
            plot_options['heatmap']['dataLabels'] = {}
        if 'enabled' not in plot_options['heatmap']['dataLabels']:
            plot_options['heatmap']['dataLabels']['enabled'] = True
        return plot_options

    def get_plot_options_json(self):
        plot_options = self.get_plot_options()
        return json.dumps(plot_options, cls=JSONEncoderForHTML)
