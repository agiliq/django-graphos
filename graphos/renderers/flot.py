import json

class LineChart(object):
    """ LineChart """

    def __init__(self, series=[], options={}, **kwargs):
        self.series = series
        self.options = options

    def set_header(self):
        pass

    def get_series_json(self):
        return json.dumps(self.series)

    def get_options_json(self):
        return json.dumps({})

    def get_template(self):
        template = 'charts/line_chart.html'
        return template