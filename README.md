Graphos
----------------

Graphos is a Django app to plot data into a live graph.

### Supported Backends:

* MongoDB
* Redis
* Django ORM

### JS Libraries used

* Jquery
* Flot

# Chart types supported

* Line chart
* Bar chart

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

### Supported DataSources

* SimpleDataSource - Creating charts from Python data structure
* CSVDataSource - Creating charts from CSV files



### Examples

#### Generating a plot from python list

    data =  [
            ['Year', 'Sales', 'Expenses'],
            [2004, 1000, 400],
            [2005, 1170, 460],
            [2006, 660, 1120],
            [2007, 1030, 540]
        ]
    Chart = LineChart(SimpleDataSource(data=data), html_id="line_chart")

#### Generating a plot from CSV file
TODO

#### Generating a plot from the ORM
Todo

#### Generating a plot from Redis
Todo

#### Generating a plot from MongoDB
Todo

### Installation
Todo - need to publish the app at Pypi after competion

### License

BSD

