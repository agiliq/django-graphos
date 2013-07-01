Creating custom charts
---------------------------

You may need to create custom charts in two scenarios:

1. You want to use a charting libary we do not support.
2. You need more control over the html than ``chart.as_html`` provides.

To customize html for an existing chart type, you will generally create a new template.::

    from graphos.renderers import gchart

    class CustomGchart(gchart.LineChart):
        def get_template(self):
            return "demo/gchart_line.html"

To create a chart for a new charting backend, create a new class extending ``BaseChart``. This class needs to return the rendrered htmls from ``as_html`` method.

However in most of the cases you will override the ``get_templates`` method.