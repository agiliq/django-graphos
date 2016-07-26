from .models import Account


DB_HOST = ["localhost"]
DB_PORT = 27017


def get_db(db_name):
    import pymongo
    DB_HOST = ["localhost"]
    DB_PORT = 27017
    db = pymongo.Connection(DB_HOST, DB_PORT)[db_name]
    return db


def get_mongo_cursor(db_name, collection_name, max_docs=100):
    import pymongo
    db = pymongo.Connection(host=DB_HOST,
                            port=DB_PORT)[db_name]
    collection = db[collection_name]
    cursor = collection.find()
    count = cursor.count
    if callable(count):
        count = count()
    if count >= max_docs:
        cursor = cursor[0:max_docs]
    return cursor


data = [
       ['Year', 'Sales', 'Expenses', 'Items Sold', 'Net Profit'],
       ['2004', 1000, 400, 100, 600],
       ['2005', 1170, 460, 120, 710],
       ['2006', 660, 1120, 50, -460],
       ['2007', 1030, 540, 100, 490],
       ]

candlestick_data = [['Mon', 20, 28, 38, 45],
                    ['Tue', 31, 38, 55, 66],
                    ['Wed', 50, 55, 77, 80],
                    ['Thu', 77, 77, 66, 50],
                    ['Fri', 68, 66, 22, 15]]

treemap_data = [
          ['Location', 'Parent', 'Market trade volume (size)', 'Market increase/decrease (color)'],
          ['Global',    None,                 0,                               0],
          ['America',   'Global',             0,                               0],
          ['Europe',    'Global',             0,                               0],
          ['Asia',      'Global',             0,                               0],
          ['Australia', 'Global',             0,                               0],
          ['Africa',    'Global',             0,                               0],
          ['Brazil',    'America',            11,                              10],
          ['USA',       'America',            52,                              31],
          ['Mexico',    'America',            24,                              12],
          ['Canada',    'America',            16,                              -23],
          ['France',    'Europe',             42,                              -11],
          ['Germany',   'Europe',             31,                              -2],
          ['Sweden',    'Europe',             22,                              -13],
          ['Italy',     'Europe',             17,                              4],
          ['UK',        'Europe',             21,                              -5],
          ['China',     'Asia',               36,                              4],
          ['Japan',     'Asia',               20,                              -12],
          ['India',     'Asia',               40,                              63],
          ['Laos',      'Asia',               4,                               34],
          ['Mongolia',  'Asia',               1,                               -5],
          ['Israel',    'Asia',               12,                              24],
          ['Iran',      'Asia',               18,                              13],
          ['Pakistan',  'Asia',               11,                              -52],
          ['Egypt',     'Africa',             21,                              0],
          ['S. Africa', 'Africa',             30,                              43],
          ['Sudan',     'Africa',             12,                              2],
          ['Congo',     'Africa',             10,                              12],
          ['Zaire',     'Africa',             8,                               10]]

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
