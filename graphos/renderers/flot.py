import json

class LineChart(object):
    """ LineChart """

    # data = [
    #             ['Year', 'Sales', 'Expenses'],
    #             ['2004',  1000,      400],
    #             ['2005',  1170,      460],
    #             ['2006',  660,       1120],
    #             ['2007',  1030,      540]
    #         ]


    def __init__(self, data=[], options={}, **kwargs):
        self.data = data
        self.options = options

    def set_header(self):
        pass

    def get_series_json(self):
        return json.dumps(self.data)

    def get_options_json(self):
        return json.dumps({})

    def get_template(self):
        template = 'charts/line_chart.html'
        return template