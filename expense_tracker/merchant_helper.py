from flask import Flask, g, request
from flask_restful import Resource, Api
from bson.json_util import dumps
from expense_tracker.db_helper import db_helper
import os
import markdown
import datetime
import uuid


class MerchantModel():
    def __init__(self, _id, name):
        self._id = _id
        self.name = name

    def __repr__(self):
        return '<MerchantModel(identifier={self.identifier!r})>'


class Merchants(Resource):
    def __init__(self):
        self.db = db_helper().get_db()

    def get(self):
        merchants = dumps(list(self.db.merchants.find({})))
        return {'message': 'Success', 'data': merchants}


class Merchant(Resource):
    def __init__(self):
        self.db = get_db()

    def get(self, identifier):

        merchant = self.db.merchants.find_one(
            {'identifier': identifier})

        if not merchant:
            return {'message':
                    'Record not found for merchant: %s' % identifier}, 400

        return {'message': 'Success', 'data': dumps(merchant)}, 200
