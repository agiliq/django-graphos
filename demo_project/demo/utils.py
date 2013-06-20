import pymongo

from .models import Account


DB_HOST = ["localhost"]
DB_PORT = 27017


def get_db(db_name):
    DB_HOST = ["localhost"]
    DB_PORT = 27017
    db = pymongo.Connection(DB_HOST, DB_PORT)[db_name]
    return db


def get_mongo_cursor(db_name, collection_name, max_docs=100):
    db = pymongo.Connection(host=DB_HOST,
                            port=DB_PORT)[db_name]
    collection = db[collection_name]
    cursor = collection.find()
    if cursor.count >= max_docs:
        cursor = cursor[0:max_docs]
    return cursor


data = [
       ['Year', 'Sales', 'Expenses', 'Items Sold', 'Net Profit'],
       ['2004', 1000, 400, 100, 600],
       ['2005', 1170, 460, 120, 310],
       ['2006', 660, 1120, 50, -460],
       ['2007', 1030, 540, 100, 200],
       ]

candlestick_data = [['Mon', 20, 28, 38, 45],
                    ['Tue', 31, 38, 55, 66],
                    ['Wed', 50, 55, 77, 80],
                    ['Thu', 77, 77, 66, 50],
                    ['Fri', 68, 66, 22, 15]]

mongo_series_object_1 = [[440, 39],
                         [488, 29.25],
                         [536, 28],
                         [584, 29],
                         [632, 33.25],
                         [728, 28.5],
                         [776, 33.25],
                         [824, 28.5],
                         [872, 31],
                         [920, 30.75],
                         [968, 26.25]]

mongo_series_object_2 = [[400, 4],
                         [488, 0],
                         [536, 20],
                         [584, 8],
                         [632, 2],
                         [680, 36],
                         [728, 0],
                         [776, 0],
                         [824, 0],
                         [872, 4],
                         [920, 1],
                         [968, 0]]

mongo_data = [{'data': mongo_series_object_1, 'label': 'hours'},
              {'data': mongo_series_object_2, 'label': 'hours'}]


def create_demo_accounts():
    Account.objects.all().delete()
    # Create some rows
    Account.objects.create(year="2004", sales=1000,
                           expenses=400, ceo="Welch")
    Account.objects.create(year="2005", sales=1170,
                           expenses=460, ceo="Jobs")
    Account.objects.create(year="2006", sales=660,
                           expenses=1120, ceo="Page")
    Account.objects.create(year="2007", sales=1030,
                           expenses=540, ceo="Welch")
    Account.objects.create(year="2008", sales=2030,
                           expenses=1540, ceo="Zuck")
    Account.objects.create(year="2009", sales=2230,
                           expenses=1840, ceo="Cook")


def create_demo_mongo():
    accounts = get_db("accounts")
    docs = accounts.docs
    docs.drop()

    docs = accounts.docs
    header = data[0]
    data_only = data[1:]
    for row in data_only:
        docs.insert(dict(zip(header, row)))
