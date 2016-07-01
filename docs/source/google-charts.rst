Using Google chart api with graphos
==========================================

Include the JS in the template::

    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
        google.load("visualization", "1", {packages:["corechart"]});
    </script>

Create a data source.::

    from graphos.sources.model import ModelDataSource
    queryset = Account.objects.all()
    data_source = ModelDataSource(queryset,
                                      fields=['year', 'sales'])


Pass the ``data_source`` to a `gchart`::

    from graphos.renderers import gchart
    chart = gchart.LineChart(data_source)

You can render this chart in the template by ``{{ point_chart.as_html }}``.

Supported chart types
--------------------------

* Area chart
* Bar chart
* Candlestick charts
* Column chart
* Line chart
* Pie chart