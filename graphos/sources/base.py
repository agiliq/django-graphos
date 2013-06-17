"""Base Plot Data Handler"""

from ..exceptions import GraphosException


class BaseDataSource(object):
    def __init__(*args, **kwargs):
        pass

    def get_data(self):
        "Get all the data. Subclasses should override this"
        raise GraphosException("Not Implemented")

    def get_header(self):
        "Get the header - First row. Subclasses should override this"
        raise GraphosException("Not Implemented")

    def get_first_column(self):
        "Get the first column. Generally would be the x axis."
        "Subclasses should override this"
        raise GraphosException("Not Implemented")
