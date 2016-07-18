from .base import BaseDataSource


class SimpleDataSource(BaseDataSource):
    def __init__(self, data):
        """
        : param data: :type list of lists
        Example usage:
            data = [
               ['Year', 'Sales', 'Expenses', 'Items Sold', 'Net Profit'],
               ['2004', 1000, 400, 100, 600],
               ['2005', 1170, 460, 120, 310],
               ['2006', 660, 1120, 50, -460],
               ['2007', 1030, 540, 100, 200],
            ]
            sd = SimpleDataSource(data)
        """
        self.data = data

    def get_data(self):
        return self.data

    def get_header(self):
        return self.data[0]

    def get_first_column(self):
        """
        Get the first column. Generally would be the x axis.
        : return: :type list of strings
        Example:
        For the example shown in __init__, it would return the following:
            ['2004', '2005', '2006', '2007']
        """
        data_not_header = self.data[1:]
        return [el[0] for el in data_not_header]
