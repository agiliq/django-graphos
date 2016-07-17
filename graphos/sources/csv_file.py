from .simple import SimpleDataSource

import csv

class CSVDataSource(SimpleDataSource):
    "A data source for CSV files"
    def __init__(self, csv_file, fields=None):
        """csv_file: A file like object which should be charted
        """
        reader = csv.reader(csv_file)
        data =[row for row in reader]
        self.data = data
        self.fields = fields
