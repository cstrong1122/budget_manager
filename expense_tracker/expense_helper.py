from flask import Flask, g, request
from flask_restful import Resource, Api
from bson.json_util import dumps
from expense_tracker.db_helper import db_helper
from bson.objectid import ObjectId
from marshmallow import Schema, fields, post_load
import datetime
import uuid
import json


class ExpenseSchema(Schema):
    _id = fields.Str(dump_to='identifier', load_from='identifier')
    amount = fields.Number()
    category_identifier = fields.Str()
    merchant_identifier = fields.Str()
    transaction_utc = fields.Str()

    @post_load
    def make_expense(self, data, **kwargs):
        return ExpenseModel(**data)


class ExpenseModel():
    def __init__(self, identifier, amount, category_identifier,
                 merchant_identifier, transaction_utc):
        self.identifier = identifier
        self.amount = amount
        self.category_identifier = category_identifier
        self.merchant_identifier = merchant_identifier
        self.transaction_utc = transaction_utc

    def __repr__(self):
        return '<ExpenseModel(identifier={self.identifier!r})>'


class Expenses(Resource):
    def __init__(self):
        self.db = db_helper().get_db()
        self.schema = ExpenseSchema()

    def get(self):

        dt_from = request.args.get('from')
        dt_to = request.args.get('to')
        dt_range = {}

        if dt_from:
            dt_range['$gte'] = dt_from

        if dt_to:
            dt_range['$lt'] = dt_to

        query = {'transaction_utc': dt_range}

        expenses = self.schema.dump(
            self.db.expenses.find({} if len(dt_range) == 0 else query),
            many=True)
        return {'message': 'Success', 'data': expenses}

    def post(self):

        # serialize request into json string and fail if unsuccessful
        json_data = request.get_json()
        if not json_data:
            return {'message': 'Not json data'}, 400

        req_expense_amt = json_data['amount']
        req_category_name = json_data['category_name']
        req_merchant_name = json_data['merchant_name']
        req_transaction_utc = json_data['transaction_utc']

        # check if category already exists with same name
        category_id = self.db.categories.find_one(
            {'name': req_category_name})['_id']

        # check if merchant already exists with same name
        merchant_id = self.db.merchants.find_one(
            {'name': req_merchant_name})['_id']

        with db_helper().get_dbclient().start_session() as session:
            with session.start_transaction():
                if not category_id:
                    # insert the new category
                    category_id = self.db.categories.insert_one(
                        {'name': req_category_name}).inserted_id

                if not merchant_id:
                    # insert the new merchant
                    merchant_id = self.db.merchants.insert_one(
                        {'name': req_merchant_name}).inserted_id

                # build expense here
                expense_json = {'amount': req_expense_amt,
                                'category_identifier': category_id,
                                'merchant_identifier': merchant_id,
                                'transaction_utc': req_transaction_utc}

                # insert new expense
                expense_id = self.db.expenses.insert_one(
                    expense_json).inserted_id

        data = self.schema.dump(self.db.expenses.find_one(expense_id))

        return {'message': 'Success',
                'data': data}, 201


class Expense(Resource):
    def __init__(self):
        self.db = db_helper().get_db()
        self.schema = ExpenseSchema()

    def get(self, identifier):

        expense = self.db.expenses.find_one(
            {'_id': ObjectId(identifier)})

        if not expense:
            return {'message':
                    'Record not found for identifier: %s' %
                    str(identifier)}, 400

        return {'message': 'Success', 'data': self.schema.dump(expense)}, 200
