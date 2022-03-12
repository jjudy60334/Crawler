# import pandas as pd
from pymongo import MongoClient
from crawler.logger import LoggingMixin


class MongoOperator(LoggingMixin):
    def __init__(self):
        self.conn = None
        self._collection = None
        self._db = None

    def _connect_mongo(self, host, port, username=None, password=None, db=None):
        """ A util for making a connection to mongo """

        if username and password:
            mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, str(port), db)
            self._db = MongoClient(mongo_uri)

        else:
            mongo_uri = 'mongodb://%s:%s' % (host, str(port))
            self.conn = MongoClient(host, port)
            self._db = self.conn[db]
        return self._db

    def get_collection(self, collection):
        self._collection = self.db[collection]
        return self._collection

    def read_mongo(
        self, db, collection, query={},
            host='localhost', port=27017, username=None, password=None, no_id=True):
        """ Read from Mongo and Store into DataFrame """

        # Connect to MongoDB
        db = self._connect_mongo(host=host, port=port, username=username, password=password, db=db)

        # Make a query to the specific DB and Collection
        cursor = db[collection].find(query)

        # Expand the cursor and construct the DataFrame
        df = pd.DataFrame(list(cursor))

        # Delete the _id
        if no_id:
            del df['_id']

        return df
