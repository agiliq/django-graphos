import json
import random
import string


class LineChart(object):
    """ LineChart """

    # data = [
    #             ['Year', 'Sales', 'Expenses'],
    #             ['2004',  1000,      400],
    #             ['2005',  1170,      460],
    #             ['2006',  660,       1120],
    #             ['2007',  1030,      540]
    #         ]

    def __init__(self, data_source, html_id=None, options={}, **kwargs):
        self.data_source = data_source
        self.data = data_source.get_data()
        self.header = self.data_source.get_header()
        self.options = options
        random_letter = lambda : random.choice(string.ascii_letters)
        self.html_id = html_id or "".join([random_letter() for el in range(10)])

    def _get_series(self, data):
        pass

    def set_header(self):
        pass

    def get_html_id(self):
        return self.html_id


    def get_serieses(self):
        data_only = self.data[1:]
        first_column = [el[0] for el in data_only]
        serieses = []
        for i in range(1, len(self.header)):
            current_column = [el[i] for el in data_only]
            current_series = zip(first_column, current_column)
            serieses.append(current_series)
        return serieses

    def get_serieses_json(self):
        return json.dumps(self.get_serieses())

    def get_options_json(self):
        return json.dumps({})

    def get_template(self):
        template = 'charts/line_chart.html'
        return template
