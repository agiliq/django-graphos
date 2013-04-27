""" Model Plot Data Handler"""

from .base_plot import BaseDataSource


class ModelDataSource(BaseDataSource):

    model_name = ''
    field_name = ''



    def __init__(self, quertyset):

        self.model_name = model_name
        self.field_name = field_name

        super(ModelPlotDataHandler, self).__init__(
            id, model_name, field_name, count, *args, **kwargs)


    def get_data(self):
        data = [
          ['Year', 'Sales', 'Expenses'],
          ['2004',  1000,      400],
          ['2005',  1170,      460],
          ['2006',  660,       1120],
          ['2007',  1030,      540]
        ]

        return data

    def get_header(self):
        return ['Year', 'Sales', 'Expenses']

    def get_first_values_column(self):
        return ("2004", "2005", "2006", "2007")
