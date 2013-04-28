""" Mongodb Plot Data Source """

from .base import BaseDataSource


class MongoDBDataSource(BaseDataSource):
    """ MongoDBDataSource """
    def __init__(self, data, *args, **kwargs):
        self.data = data

    def get_data(self):
        return self.data

    def get_header(self):
        pass

    def get_first_column(self):
        pass
