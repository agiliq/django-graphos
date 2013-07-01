Using flot with Django-graphos
==========================================

Include the js in your html::

    <script src="{% sttaic 'js/jquery.flot.js' %}"></script>

Create a data source.::

    from graphos.sources.model import ModelDataSource
    queryset = Account.objects.all()
    data_source = ModelDataSource(queryset,
                                      fields=['year', 'sales'])


Pass the ``data_source`` to a flot Chart::

    from graphos.renderers import flot
    chart = flot.LineChart(data_source)

You can render this chart in the template by ``{{ point_chart.as_html }}``.

Supported chart types
--------------------------

* Line
* Bar
* Point
