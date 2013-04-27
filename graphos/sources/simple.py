from .base import BaseDataSource


class SimpleDataSource(BaseDataSource):
    def __init__(self, data):
        self.data = data

    def get_data(self):
        return self.data

    def get_header(self):
        return self.data[0]

    def get_first_column(self):
        data_not_header = self.data[1:]
        return [el[0] for el in data_not_header]
