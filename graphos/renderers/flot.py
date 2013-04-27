import json
import random
import string


class Chart(object):

    def __init__(self, data_source, html_id=None, options={}, *args, **kwargs):
        self.data_source = data_source
        self.data = data_source.get_data()
        self.header = data_source.get_header()
        self.options = options
        random_letter = lambda: random.choice(string.ascii_letters)
        self.html_id = html_id or "".join([random_letter()
                                          for el in range(10)])

    def get_html_id(self):
        return self.html_id

    def get_serieses(self):
        pass

    def get_options(self):
        pass

    def get_template(self):
        pass

    def get_serieses_json(self):
        return json.dumps(self.get_serieses())

    def get_options_json(self):
        return json.dumps(self.options)


class LineChart(Chart):
    """ LineChart """

    # data = [
    #             ['Year', 'Sales', 'Expenses'],
    #             ['2004',  1000,      400],
    #             ['2005',  1170,      460],
    #             ['2006',  660,       1120],
    #             ['2007',  1030,      540]
    #         ]

    def __init__(self, *args, **kwargs):
        super(LineChart, self).__init__(*args, **kwargs)

    def get_serieses(self):
        data_only = self.data[1:]
        first_column = [el[0] for el in data_only]
        serieses = []
        for i in range(1, len(self.header)):
            current_column = [el[i] for el in data_only]
            current_series = zip(first_column, current_column)
            serieses.append(current_series)
        return serieses

    def get_series_objects(self):
        series_objects = []
        serieses = self.get_serieses()
        for i in range(1, len(self.header)):
            series_object = {}
            series_object['label'] = self.header[i]
            series_object['data'] = serieses[i-1]
            series_objects.append(series_object)
        return series_objects

    def get_series_objects_json(self):
        return json.dumps(self.get_series_objects())

    def get_options(self):
        pass

    def get_template(self):
        template = 'charts/line_chart.html'
        return template
