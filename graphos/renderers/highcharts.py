from .base import BaseChart
import json
from collections import defaultdict, OrderedDict
from decimal import Decimal
from copy import deepcopy
import sys

from django.template.loader import render_to_string
from ..utils import JSONEncoderForHTML
from ..exceptions import GraphosException


class BaseHighCharts(BaseChart):
    """
    This has been written with categorical x axis in mind.
    This assumes that first column would be non-numeric, and assumes that every other column tells data for a series and would be numeric. If this assumption is violated, chart wouldn't be proper.
    """
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
        if 'annotation' in options:
            data = self.get_data()
            annotation_list = options['annotation']
            for i, name in enumerate(series_names):
                new_data = []
                if name in annotation_list:
                    data_list = column(data, i + 1)[1:]
                    for k in data_list:
                        temp_data = {}
                        for j in annotation_list[name]:
                            if k == j['id']:
                                temp_data['y'] = k
                                temp_data['dataLabels'] = {'enabled': True, 'format': j['value']}
                            else:
                                temp_data['y'] = k
                        new_data.append(temp_data)
                    series = {"name": name, "data": new_data}
                else:
                    series = {"name": name, "data": column(data, i + 1)[1:]}
                if 'colors' in options and len(options['colors']) > i:
                    series['color'] = options['colors'][i]
                serieses.append(series)
        else:
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
        This would return ['2004', '2005', '2006', '2007']
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

    def get_plot_options(self):
        plot_options = self.get_options().get('plotOptions', {})
        return plot_options

    def get_plot_options_json(self):
        plot_options = self.get_plot_options()
        return json.dumps(plot_options, cls=JSONEncoderForHTML)

    def get_x_axis_title(self):
        return self.get_data()[0][0]

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

    def get_y_axis_title(self):
        data = self.get_data()
        # For single series data, set y-axis title to header of first series
        # For multi series data, it's responsibility of user to set yAxis title.
        if len(data[0]) == 2:
            return data[0][1]
        else:
            return "Values"

    def get_y_axis(self):
        y_axis = self.get_options().get('yAxis', {})
        if not 'title' in y_axis:
            y_axis['title'] = {}
        if not 'text' in y_axis['title']:
            y_axis['title']['text'] = self.get_y_axis_title()
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
    def __init__(self, *args, **kwargs):
        super(ScatterChart, self).__init__(*args, **kwargs)
        types = [int, float, Decimal]
        if not sys.version_info > (3,):
            types.append(long)
        data = self.get_data()
        if type(data[1][1]) in types:
            self.series_type = 'single_series'
        else:
            self.series_type = 'multi_series'
        if len(data[0]) < 3:
            raise GraphosException("Scatter chart needs atleast 3 columns")
        if len(data[0]) > 4:
            raise GraphosException("Scatter chart can't have more than 4 columns")

    def get_chart_type(self):
        return "scatter"

    def get_series(self):
        if self.series_type == 'single_series':
            serieses = self.calculate_single_series()
        else:
            serieses = self.calculate_multi_series()
        return serieses

    def calculate_single_series(self):
        temp_name = self.get_data()[0][0]
        data = [{temp_name: row[0],"x": row[1],'y': row[2]} for row in self.get_data()[1:]]
        # TODO: What should be series_name in this case? Should it be read from options?
        # TODO: Add color ability
        series = {'data': data, 'name': self.get_data()[0][0]}
        return [series]

    def calculate_multi_series(self):
        temp_name = self.get_data()[0][0]
        data = self.get_data()[1:]
        name_to_points_dict = defaultdict(list)
        for row in data:
            series_name = row[1]
            l = {temp_name: row[0],"x": row[2],"y": row[3]}
            name_to_points_dict[series_name].append(l)
        serieses = []
        for series_name, points in name_to_points_dict.items():
            series = {}
            series['name'] = series_name
            series['data'] = points
            # TODO: Add color ability
            serieses.append(series)
        return serieses

    def get_x_axis_title(self):
        if self.series_type == 'single_series':
            return self.get_data()[0][1]
        else:
            return self.get_data()[0][2]

    def get_x_axis(self):
        x_axis = super(ScatterChart, self).get_x_axis()
        # categories doesn't make sense for Scatter chart because x axis doesn't have categories. Instead it has values
        del x_axis['categories']
        return x_axis

    def get_y_axis_title(self):
        if self.series_type == 'single_series':
            return self.get_data()[0][2]
        else:
            return self.get_data()[0][3]


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

    def get_plot_options(self):
        plot_options = self.get_options().get('plotOptions', {})
        if not 'pie' in plot_options:
            plot_options['pie'] = {}
        if 'showInLegend' not in plot_options['pie']:
            plot_options['pie']['showInLegend'] = True
        if 'dataLabels' not in plot_options['pie']:
            plot_options['pie']['dataLabels'] = {'enabled': False}
        return plot_options

    def get_chart_type(self):
        return "pie"


class DonutChart(PieChart):
    def get_chart(self):
        chart = super(DonutChart, self).get_chart()
        chart['options3d'] = {'enabled': True, 'alpha': 45}
        return chart

    def get_plot_options(self):
        plot_options = self.get_options().get('plotOptions', {})
        plot_options['pie'] = {'innerSize': 100, 'depth': 45}
        return plot_options


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
        # TODO: This is overriding any thing set in yAxis. Fix
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
        types = [int, float, Decimal]
        if not sys.version_info > (3,):
            types.append(long)
        if type(first_column) in types and type(second_column) in types:
            self.is_lat_long = True
        if not self.is_lat_long:
            value_to_check_for_series_type = self.get_data()[1][1]
        else:
            value_to_check_for_series_type = self.get_data()[1][2]
        if type(value_to_check_for_series_type) in types:
            self.series_type = 'single_series'
        else:
            self.series_type = 'multi_series'

    def get_series(self):
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
            if chart_type == 'mappoint':
                series['lineWidth'] = 2
            i += 1
        if chart_type == 'mapbubble' or chart_type == 'mappoint':
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
            elif chart_type == 'mappoint':
                # It must be a lat/lon chart because points only make sense for lat/lon
                if not self.is_lat_long:
                    raise GraphosException("For mappoint chart, you must use lat/lon")
                else:
                    region_detail = {'lat': kv[0], 'lon': kv[1]}
            elif chart_type == 'map':
                region_detail = {'code': kv[0], 'value': kv[1]}
            first_series['data'].append(region_detail)
        join_by = self.get_options().get('joinBy', 'hc-key')
        first_series['joinBy'] = [join_by, 'code']
        first_series['name'] = self.get_series_name()
        serieses = []
        serieses.append(first_series)
        if chart_type == 'mapbubble' or chart_type == 'mappoint':
            just_for_sake_series = {}
            just_for_sake_series['name'] = 'Basemap'
            just_for_sake_series['type'] = 'map'
            just_for_sake_series['showInLegend'] = False
            serieses.insert(0, just_for_sake_series)
        if chart_type == 'mappoint':
            first_series['lineWidth'] = 2
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

    def get_chart_type(self):
        # If you are using mapbubble, ensure you don't set allAreas to False.
        # Also if you are setting mapbubble for a multi series chart, then probably you should set zKey too to get different bubble sizes.
        if self.is_lat_long and self.get_options().get("map_type") != 'mappoint':
            return "mapbubble"
        else:
            return self.get_options().get("map_type", "map")


def column(matrix, i):
    return [row[i] for row in matrix]


def pie_column(matrix, i):
    return [{'name':row[0],'y':row[i]} for row in matrix]

class HeatMap(BaseHighCharts):

    def get_series(self):
        tempdata = deepcopy(self.get_data())
        tempdata = tempdata[1:]
        serieses = []
        new_list = []
        X_len = len(tempdata)
        Y_len = len(tempdata[0])
        value_list = tempdata
        for row in value_list:
            del row[0]
        for i in range(0,X_len):
            for j in range(0, Y_len-1):
                new_list.append([i, j, value_list[i][j]])
        data = new_list
        serieses.append({'data': data})
        return serieses

    def get_y_axis(self):
        # TODO: Check if this should call super()
        categories = self.get_data()[0][1:]
        y_axis = {'categories': categories}
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


class Funnel(BaseHighCharts):

    def get_series(self):
        serieses = []
        data = self.get_data()[1:]
        serieses.append({"data": data})
        return serieses

    def get_chart_type(self):
        return "funnel"

    def get_plot_options(self):
        plot_options = self.get_options().get('plotOptions', {})
        if not 'funnel' in plot_options:
            plot_options['funnel'] = {}
        if 'neckWidth' not in plot_options['funnel']:
            plot_options['funnel']['neckWidth'] = '30%'
        if 'neckHeight' not in plot_options['funnel']:
            plot_options['funnel']['neckHeight'] = '25%'
        if 'dataLabels' not in plot_options['funnel']:
            plot_options['funnel']['dataLabels'] = {}
        if 'enabled' not in plot_options['funnel']['dataLabels']:
            plot_options['funnel']['dataLabels']['enabled'] = True
        if 'softConnector' not in plot_options['funnel']['dataLabels']:
            plot_options['funnel']['dataLabels']['softConnector'] = True
        return plot_options


color_picker_list = ['#7cb5ec', '#434348', '#90ed7d', '#f7a35c', '#8085e9', '#f15c80', '#e4d354', '#2b908f',
                     '#f45b5b', '#91e8e1', '#42f44e', '#d61532', '#f1f442', '#ee42f4', '#4286f4', '#B96A30',
                     '#396932', '#B6CFEB', '#72F998', '#4F7030', '#563FF7', '#280B65', '#9AC7F4', '#D00E4E',
                     '#00f442', '#ee42f4', '#E91605', '#B96000', '#396932', '#B6CFEB', '#72F458', '#4F7030',
                     '#563FF7', '#280B65', '#9AC7F4', '#D7FE4E', '#42f44e', '#d61532', '#f1f400', '#ee42f4',
                     '#E99905', '#B96A30', '#396932', '#B6CFEB', '#72F458', '#4F7030', '#563FF7', '#280B65',
                     '#9AC7F4', '#D7FE4E', '#42f44e', '#d61532', '#f1f442', '#ee42f4', '#E91605', '#B96A30',
                     '#396932', '#B6CFEB', '#729958', '#4F7030', '#563FF7', '#280B65', '#9AC7F4', '#D7FE4E',
                     '#42f44e', '#d61532', '#f1f442', '#ee42f4', '#E91605', '#B96A30', '#396932', '#B6CFEB',
                     '#72F458', '#4F7030', '#563FF7', '#280B65', '#9AC7F4', '#D7A!4E', '#42f44e', '#d61532',
                     '#f1f442', '#ee42f4', '#E91605', '#B96A30', '#396932', '#B6CFEB', '#72F458', '#4F7030',
                     '#563FF7', '#280B65', '#9AC7F4', '#D7FE4E', '#42f44e', '#d61532', '#f1f442', '#ee42f4',
                     '#E91605', '#B96A30', '#39FF32', '#B6CFEB', '#72F458', '#4F7030', '#563FF7', '#280B65',
                     '#9AC7F4', '#D7FE4E', '#40744e', '#ZZ1532', '#f1f442', '#ee42f4', '#E91605', '#B96A30',
                     '#3905932', '#B6CFEB', '#72F458', '#4F7030', '#563FF7', '#280B65', '#BBC7F4', '#D7FE4E']

def nested_list_to_tree(data):
    treemap_data = data
    l = treemap_data[1:]
    root = {}
    for path in l:
        parent = root
        for n in path:
            parent = parent.setdefault(n, {})
    root = OrderedDict(root)
    return root

def generate_treemap_data(root, no_of_column):
    final_data = []
    counter_0 = 0
    counter_1 = 0
    counter_2 = 0
    if no_of_column == 2:
        for i, j in root.items():
            parent_data = {}
            parent_data['id'] = 'id_' + str(counter_0)
            parent_data['name'] = i
            parent_data['color'] = color_picker_list[counter_0]
            key = list(j.keys())
            parent_data['value'] = key[0]
            final_data.append(parent_data)
            counter_0 += 1
    if no_of_column == 3:
        for i, j in root.items():
            parent_data = {}
            parent_value = 0
            parent_data['id'] = 'id_' + str(counter_0)
            parent_data['name'] = i
            parent_data['color'] =  color_picker_list[counter_0]
            parent_id = 'id_' + str(counter_0)
            for k, l in j.items():
                data = {}
                data['id'] = parent_id + str(counter_1)
                data['name'] = k
                data['parent'] = parent_id
                data['color'] = color_picker_list[counter_0]
                key = list(l.keys())
                data['value'] = key[0]
                final_data.append(data)
                parent_value += key[0]
                counter_1 += 1
            parent_data['value'] = parent_value
            final_data.append(parent_data)
            counter_0 += 1
    if no_of_column == 4:
        for i, j in root.items():
            parent_data = {}
            parent_value = 0
            parent_data['id'] = 'id_' + str(counter_0)
            parent_data['name'] = i
            parent_data['color'] = color_picker_list[counter_0]
            parent_id = 'id_' + str(counter_0)
            for k, l in j.items():
                data = {}
                data['id'] = parent_id + str(counter_1)
                data['name'] = k
                data['parent'] = parent_id
                data['color'] = color_picker_list[counter_0]
                child_id = parent_id + str(counter_1)
                final_data.append(data)
                counter_1 += 1
                for m, na in l.items():
                    data = {}
                    data['id'] = child_id + str(counter_1)
                    data['name'] = m
                    data['parent'] = child_id
                    data['color'] = color_picker_list[counter_0]
                    key = list(na.keys())
                    data['value'] = key[0]
                    final_data.append(data)
                    counter_2 += 1
                    parent_value += key[0]
            parent_data['value'] = parent_value
            final_data.append(parent_data)
            counter_0 += 1
    return final_data


def generate_pie_donut_data(root, no_of_column):
    final_data = []
    counter_0 = 0
    list_0 = []
    list_1 = []
    if no_of_column == 2:
        for i, j in root.items():
            parent_data = {}
            parent_data['name'] = i
            parent_data['color'] = color_picker_list[counter_0]
            key = list(j.keys())
            parent_data['y'] = key[0]
            final_data.append(parent_data)
            counter_0 += 1
        return final_data
    if no_of_column == 3:
        for i, j in root.items():
            parent_data = {}
            parent_value = 0
            parent_data['name'] = i
            parent_data['color'] = color_picker_list[counter_0]
            for k, l in j.items():
                data = {}
                data['name'] = k
                data['color'] = color_picker_list[counter_0]
                key= list(l.keys())
                data['y'] = key[0]
                parent_value += key[0]
                list_1.append(data)
            counter_0 += 1
            parent_data['y'] = parent_value
            list_0.append(parent_data)
        final_data.append(list_0)
        final_data.append(list_1)
        return final_data



class TreeMap(BaseHighCharts):

    def get_series(self):
        serieses = []
        data = self.get_data()
        root = nested_list_to_tree(data)
        no_of_column = len(data[0])
        final_data = generate_treemap_data(root, no_of_column)
        data = final_data
        serieses.append({"data": data})
        return serieses

    def get_chart_type(self):
        return "treemap"

    def get_plot_options(self):
        plot_options = self.get_options().get('plotOptions', {})
        if not 'treemap' in plot_options:
            plot_options['treemap'] = {}
        if 'type' not in plot_options['treemap']:
            plot_options['treemap']['type'] = 'treemap'
        if 'layoutAlgorithm' not in plot_options['treemap']:
            plot_options['treemap']['layoutAlgorithm'] = 'squarified'
        if 'allowDrillToNode' not in plot_options['treemap']:
            plot_options['treemap']['allowDrillToNode'] = True
        if 'animationLimit' not in plot_options['treemap']:
            plot_options['treemap']['animationLimit'] = 1000
        if 'levelIsConstant' not in plot_options['treemap']:
            plot_options['treemap']['levelIsConstant'] = False
        if 'dataLabels' not in plot_options['treemap']:
            plot_options['treemap']['dataLabels'] = {'enabled': False}
        if 'levels' not in plot_options['treemap']:
            plot_options['treemap']['levels'] = [{'level': 1,'dataLabels': {'enabled': True},'borderWidth': 3}]
        return plot_options

    def get_js_template(self):
        return "graphos/highcharts/js_treemap.html"


class PieDonut(BaseHighCharts):

    def get_series(self):
        serieses = []
        data = self.get_data()
        root = nested_list_to_tree(data)
        no_of_column = len(data[0])
        final_data = generate_pie_donut_data(root, no_of_column)
        result = final_data
        if no_of_column == 2:
            serieses.append({"name":data[0][0],"data": result,"size": '100%'})
        if no_of_column == 3:
            serieses.append({'name': data[0][0], 'data': result[0], 'size': '60%','dataLabels': {'enabled': False}, 'showInLegend': True})
            serieses.append({'name':  data[0][1], 'data': result[1], 'size': '80%','innerSize': '60%'})
        return serieses

    def get_chart_type(self):
        return "pie"


class Bubble(BaseHighCharts):

    def __init__(self, *args, **kwargs):
        super(Bubble, self).__init__(*args, **kwargs)
        types = [int, float, Decimal]
        if not sys.version_info > (3,):
            types.append(long)
        data = self.get_data()
        if type(data[1][1]) in types:
            self.series_type = 'single_series'
        else:
            self.series_type = 'multi_series'
        if len(data[0]) < 4:
            raise GraphosException("Bubble chart needs atleast 4 columns")
        if len(data[0]) > 5:
            raise GraphosException("Bubble chart can't have more than 5 columns")

    def get_series(self):
        if self.series_type == 'single_series':
            serieses = self.calculate_single_series()
        else:
            serieses = self.calculate_multi_series()
        return serieses

    def calculate_single_series(self):
        temp_name = self.get_data()[0][0]
        data = [{temp_name: row[0], "x": row[1], 'y': row[2],'z': row[3]} for row in self.get_data()[1:]]
        # TODO: What should be series_name in this case? Should it be read from options?
        # TODO: Add color ability
        series = {'data': data, 'name': self.get_data()[0][0]}
        return [series]

    def calculate_multi_series(self):
        temp_name = self.get_data()[0][0]
        data = self.get_data()[1:]
        name_to_points_dict = defaultdict(list)
        for row in data:
            series_name = row[1]
            l = {temp_name: row[0], "x": row[2], "y": row[3],"z": row[4]}
            name_to_points_dict[series_name].append(l)
        serieses = []
        for series_name, points in name_to_points_dict.items():
            series = {}
            series['name'] = series_name
            series['data'] = points
            # TODO: Add color ability
            serieses.append(series)
        return serieses

    def get_x_axis_title(self):
        if self.series_type == 'single_series':
            return self.get_data()[0][1]
        else:
            return self.get_data()[0][2]

    def get_x_axis(self):
        x_axis = super(Bubble, self).get_x_axis()
        # categories doesn't make sense for Bubble chart because x axis doesn't have categories. Instead it has values
        del x_axis['categories']
        return x_axis

    def get_y_axis_title(self):
        if self.series_type == 'single_series':
            return self.get_data()[0][2]
        else:
            return self.get_data()[0][3]

    def get_chart_type(self):
        return "bubble"
