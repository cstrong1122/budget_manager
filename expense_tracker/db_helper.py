from pymongo import MongoClient
from flask import g
from expense_tracker.config_helper import config_helper


class db_helper:
    def __init__(self):
        self.client = MongoClient(
            config_helper().connection_strings['mongo_db_expensetracker'])

    def get_dbclient(self):
        if 'db' not in g:
            return self.client
        return g.db.client

    def get_db(self):
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = self.client.expensetracker
        return db

    def close_db(self):
        if self.client is not None:
            self.client.close()
