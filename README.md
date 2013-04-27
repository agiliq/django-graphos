Graphos
----------------

Graphos is a Django app to plot data into a live graph.

### Supported Backends:

* Python Nested lists
* CSV Files
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

### License

BSD

