Doing Ajax with Graphos
==========================================

Graphos plays well with ajax interactions. There are two ways you can replace a graph object.

1. Render ``chart.as_html`` in the views. Return and replace the ``DOM``.
2. Calculate the ``chart.get_data``, return the JSON. Redraw the chart using ``$.plot`` or equivalent.