Creating a data source
-------------------------

If you need your chart to get data from a data source we do not natively support, writing a custom data source is easy. Once you do that, the data source can be used in any ``renderer``.

To create a new data source

1. Create a class which extends ``BaseDataSource`` or ``SimpleDataSource``
2. Make sure your class has implementation of ``get_data``, ``get_header`` and ``get_first_column``
3. ``get_data`` Should return a NxM matrix (see example data below). 



Example Data::

    data = [
           ['Year', 'Sales', 'Expenses', 'Items Sold', 'Net Profit'],
           ['2004', 1000, 400, 100, 600],
           ['2005', 1170, 460, 120, 310],
           ['2006', 660, 1120, 50, -460],
           ['2007', 1030, 540, 100, 200],
           ]