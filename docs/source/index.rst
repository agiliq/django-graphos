.. Django Graphos documentation master file, created by
   sphinx-quickstart on Thu Jun 20 19:45:15 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Django Graphos's documentation!
==========================================

Contents:

Django-graphos is a tool to create Graphs. (doh). 
There are two things which Graphos gives you over a low level graph manupulation.

It provides various data sources.

* SimpleDataSource - Use a Python list
* ModelDataSource 
* MongoDataSource

It provides various renderers.

* Flot
* Google charts
* YUI
* Morris.js
* (And more)

Graphos makes it very easy to switch between different data source and renderers.

Are you building your charts with Flot but would like to later switch to Gchart? In many cases, it might be as easy as switching an import statement. 



.. toctree::
   :maxdepth: 2

   intro
   flot
   google-charts
   ajax
   custom-data-source
   custom-charts




Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

