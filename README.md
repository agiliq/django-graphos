Graphos
----------------

[![Build Status](https://travis-ci.org/agiliq/django-graphos.png)](https://travis-ci.org/agiliq/django-graphos)

Graphos is a Django app to normalize data to create beautiful charts. It provides a JS agnostic way to work with charts.

* Demo: [http://agiliq.com/demo/graphos/](http://agiliq.com/demo/graphos/).  
* Docs: [http://agiliq.com/docs/django-graphos/](http://agiliq.com/docs/django-graphos/).

### Supported Backends:

* Python Nested lists
* CSV Files
* MongoDB
* Django ORM

### Charting API Supported

* [Flot](http://flotcharts.org)
* [Google Charts API](https://developers.google.com/chart/)
* [YUI Charts](http://yuilibrary.com/yui/docs/charts/)
* [Morris.js](http://www.oesmith.co.uk/morris.js/)
* [Highcharts](http://www.highcharts.com/)
* [Matplotlib](http://matplotlib.org/api/pyplot_api.html)

### Chart types supported

#### Flot

* Line chart
* Bar Chart
* Point Chart

#### Google Charts

* Line chart
* Bar chart
* Column chart
* Pie chart
* Area chart
* Candlestick chart
* Treemap chart
* Gauge chart

#### YUI

* Line chart
* Spline chart
* Bar chart
* Column chart
* Pie chart
* Area chart
* Areaspline chart

#### Morris.js

* Line chart
* Bar chart
* Donut chart
* Area chart

#### Highcharts

(You will need to buy a license if you use highcharts for commerical use)

* Line Chart
* Bar Chart
* Column Chart
* Pie Chart
* Area Chart

#### Matplotlib

* LineChart
* BarChart


### Demo

* Clone the project

	git clone https://github.com/agiliq/django-graphos.git

* Cd to demo directory

	cd django-graphos/demo_project/

* Create local settings.

	cp demo_project/settings/local.py-dist demo_project/settings/local.py

* Install requirements

	pip install -r requirements.txt

* Run migrate

	python manage.py migrate

* Run server

	python manage.py runserver

The installed demo app shows the various suported chart types.

In case you want to use mongo data while charting, you must have mongodb properly setup and **pymongo** installed. Make sure mongo server is running.

	mongod --dbpath ~/data/db

Mongo setup is optional and is not needed to get running with demo project.


### Overview of Plot generation

Generating a plot requires two things. A DataSource object and a Chart object.

In your view, you do something like this:

	from graphos.sources.simple import SimpleDataSource
	from graphos.renderers.gchart import LineChart

    data =  [
            ['Year', 'Sales', 'Expenses'],
            [2004, 1000, 400],
            [2005, 1170, 460],
            [2006, 660, 1120],
            [2007, 1030, 540]
        ]
    data_source = SimpleDataSource(data=data)
    chart = LineChart(data_source)
    context = {'chart': chart}
    return render(request, 'yourtemplate.html', context)

And then in the template:

    {{ chart.as_html }}

In this example we are planning to use Google chart, as is evident from the import statement in the view, we import gchart.LineChart. So we must also include the gchart javascript in our template.

    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
        google.load("visualization", "1", {packages:["corechart"]});
    </script>

So the template would look like

    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
        google.load("visualization", "1", {packages:["corechart"]});
    </script>

    {{ chart.as_html }}

If we want to use yui LineChart instead of gchart LineChart, our view would have:

	from graphos.renderers.yui import LineChart
    chart = LineChart(data_source)

And our template would inclue yui javascript and it would look like:

	<script src="http://yui.yahooapis.com/3.10.0/build/yui/yui-min.js"></script>
    {{ chart.as_html }}

See, how easy it was to switch from gchart to yui. You did not have to write or change a single line of javascript to switch from gchart to yui. All that was taken care of by as_html() of the chart object.

### Examples

#### Generating a plot from python list

    data =  [
            ['Year', 'Sales', 'Expenses'],
            [2004, 1000, 400],
            [2005, 1170, 460],
            [2006, 660, 1120],
            [2007, 1030, 540]
        ]
    from graphos.sources.simple import SimpleDataSource
    from graphos.renderers.gchart import LineChart
    chart = LineChart(SimpleDataSource(data=data))

#### Generating a plot from CSV file

    from graphos.sources.csv_file import CSVDataSource
    from graphos.renderers.yui import LineChart
    csv_file = open("hello.csv")
    chart = LineChart(CSVDataSource(csv_file))

#### Generating a plot from the ORM

    from graphos.sources.model import ModelDataSource
    from someapp.models import Accounts
    queryset = Accounts.objects.filter(foo=bar)
    chart = LineChart(ModelDataSource(queryset, fields=["year", "sales", "expenses"]))

#### Generating a plot from MongoDB
Todo

### Installation

pip install django-graphos

### Compatibility

Graphos is compatible with Python 2.7 and Python 3.3+

[available on pypi](https://pypi.python.org/pypi/django-graphos/)


### Creating new DataSource

A DataSource is a class which has these three methods.

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

If you create a class extending `SimpleDataSource`, and implement `get_data`. You get
`get_header` and `get_first_column` for free.

### Creating new Renderer

A renderer is a class which takes a  `DataSource` and can convert it to the html to display.

The only required method on a `Renderer` is `as_html`. This will convert the data to a format which can display the chart.

Generally you will convert the data to json and pass it to the template which you return.


### Handling non serializable fields

You need to override get_data() of existing DataSource and convert datetime field into something which could be serialized.

Assuming you are using a Python list as data, then you need to do:

    from graphos.sources.simple import SimpleDataSource
    class MySimpleDataSource(SimpleDataSource):
		def get_data(self):
			data = super(MySimpleDataSource, self).get_data()
			header = data[0]
			data_without_header = data[1:]
			for row in data_without_header:
				# Assuming first column contains datetime
				row[0] = row[0].year
			data_without_header.insert(0, header)
			return data_without_header

And data has

    d1 = datetime(2015, 7, 8, 1, 1)
    d2 = datetime(2016, 7, 8, 3, 1)

    data1 = [
             ['Year', 'Sales', 'Expenses', 'Items Sold', 'Net Profit'],
             [d1, 1000, 400, 100, 600],
             [d2, 1170, 460, 120, 310],
     ]

    chart = flot.LineChart(MySimpleDataSource(data=data1))

If you are planning to use queryset with ModelDataSource, then you would create following class

    from graphos.sources.model import ModelDataSource
    class MyModelDataSource(ModelDataSource):
        def get_data(self):
            data = super(MyModelDataSource, self).get_data()
            header = data[0]
            data_without_header = data[1:]
            for row in data_without_header:
                # Assuming second column contains datetime
                row[1] = row[1].year
			data_without_header.insert(0, header)
			return data_without_header

And you would use this class like:

    queryset = Account.objects.all()
    chart = flot.LineChart(MyModelDataSource(queryset=queryset, fields=['sales', 'datetime_field','expenses']))

### License

BSD
