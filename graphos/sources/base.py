"""Base Plot Data Handler"""

from ..exceptions import GraphosException


class BaseDataSource(object):

    id = ''
    count = ''
    frequency = ''
    width = ''
    height = ''
    y_max = ''
    color = ''

    def __init__(*args, **kwargs):
        pass

    def get_data(self):
        pass

