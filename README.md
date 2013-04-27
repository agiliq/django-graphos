Graphos
----------------

[![Build Status](https://travis-ci.org/agiliq/django-graphos.png)](https://travis-ci.org/agiliq/django-graphos)

Graphos is a Django app to plot data into a live graph.

### Supported Backends:

* Python Nested lists
* CSV Files
* MongoDB
* Redis
* Django ORM

### Charting API Supported

* [Flot](http://flotcharts.org)
* [Google Charts API](https://developers.google.com/chart/)
* [YUI Charts](http://yuilibrary.com/yui/docs/charts/)

### Chart types supported

#### Flot

* Line Chart

#### Google Charts

* Line chart
* Column chart

#### YUI

* Coming Soon

### Demo

Install the requirements, `manage.py runserver`.
The installed demo app shows the various suported chart types.


### Overview of Plot generation

Generating a plot requires two things. A DataSource and a Chart object.

In your view, you do something like this:

    data =  [
            ['Year', 'Sales', 'Expenses'],
            [2004, 1000, 400],
            [2005, 1170, 460],
            [2006, 660, 1120],
            [2007, 1030, 540]
        ]
    Chart = LineChart(SimpleDataSource(data=data), html_id="line_chart")

And then in the template:

    {% load graphos_tags %}

    {% plot chart %}


### Examples

#### Generating a plot from python list

    data =  [
            ['Year', 'Sales', 'Expenses'],
            [2004, 1000, 400],
            [2005, 1170, 460],
            [2006, 660, 1120],
            [2007, 1030, 540]
        ]
    Chart = LineChart(SimpleDataSource(data=data))

#### Generating a plot from CSV file

    csv_file = open("hello.csv")
    LineChart(CSVDataSource(csv_file))

#### Generating a plot from the ORM

    queryset = Accounts.objects.filter(foo=bar)
    LineChart(ModelDataSource(queryset, fields=["year", "sales", "expenses"]))


#### Generating a plot from Redis
Todo

#### Generating a plot from MongoDB
Todo

### Installation
Todo - need to publish the app at Pypi after competion


### Creating new backend

A backend is  class which has these three methods.

    get_data
    get_header
    get_first_column

`get_header` is used by a `Renderer` to create the labels.
`get_first_column` is used to set the x axis labels
`get_data` is used to get the data for display. It should always return a nested list. Eg:

    [
        ['Year', 'Sales', 'Expenses'],
        [2004, 1000, 400],
        [2005, 1170, 460],
        [2006, 660, 1120],
        [2007, 1030, 540]
    ]

If you create a class extending SimpleDataSource, and implement `get_data`. You get
`get_header` and `get_first_column` for free.


### License

BSD

