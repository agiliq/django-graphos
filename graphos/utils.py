import random
import string

import pymongo


DEFAULT_HEIGHT = 400
DEFAULT_WIDTH = 800

DB_HOST = ["localhost"]
DB_PORT = 27017


def get_random_string():
    random_letter = lambda: random.choice(string.ascii_letters)
    random_string = "".join([random_letter()
                             for el in range(10)])
    return random_string


def get_default_options(graph_type="lines"):
    """ default options """
    options = {"series": {"%s" % graph_type: {"show": "true"}},
               "legend": {"position": 'ne'},
               "title": "Chart"}
    return options


def get_db(db_name=None):
    """ GetDB - simple function to wrap getting a database
    connection from the connection pool.
    """
    return pymongo.Connection(host=DB_HOST,
                              port=DB_PORT)[db_name]


def get_mongo_cursor(db_name, collection_name, max_docs=100):
    db = get_db(db_name)
    collection = db[collection_name]
    cursor = collection.find()
    if cursor.count >= max_docs:
        cursor = cursor[0:max_docs]
    return cursor
