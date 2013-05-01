
import pymongo

DB_HOST = ["localhost"]
DB_PORT = 27017


def get_mongo_cursor(db_name, collection_name, max_docs=100):
    db = pymongo.Connection(host=DB_HOST,
                            port=DB_PORT)[db_name]
    collection = db[collection_name]
    cursor = collection.find()
    if cursor.count >= max_docs:
        cursor = cursor[0:max_docs]
    return cursor
