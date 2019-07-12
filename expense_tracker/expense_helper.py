from flask import Flask, g, request
from flask_restful import Resource, Api
from bson.json_util import dumps
from expense_tracker.db_helper import db_helper
import os
import markdown
import datetime
import uuid


class ExpenseModel():
    def __init__(self, identifier, amount, category_name, category_identifier,
                 merchant_name, merchant_identifier, transaction_utc):
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

    def get(self):

        fromDateTime = None
        toDateTime = None
        query = None

        if request.args.get('from'):
            fromDateTime = request.args.get('from')

        if request.args.get('to'):
            toDateTime = request.args.get('to')

        if fromDateTime and toDateTime:
            query = {'transaction_utc': {
                '$gte': fromDateTime, '$lt': toDateTime}}

        expenses = dumps(
            list(self.db.expenses.find({} if query is None else query)))
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

        post_expense_id = None
        post_category_id = None
        post_merchant_id = None

        is_new_category = False
        is_new_merchant = False

        # check if category already exists with same name
        existing_category = self.db.categories.find_one(
            {'name': req_category_name})

        # if the category already exists, initialize the category id
        if existing_category is not None:
            post_category_id = existing_category['identifier']
        # if it doesn't exist, insert the category and get the category id
        else:
            is_new_category = True
            # genereate the category identifier
            post_category_id = uuid.uuid4()

        # check if merchant already exists with same name
        existing_merchant = self.db.merchants.find_one(
            {'name': req_merchant_name})

        # if the merchant already exists, initialize the merchant id
        if existing_merchant is not None:
            post_merchant_id = existing_merchant['identifier']
        # if it doesn't exist, insert the merchant and get the merchant id
        else:
            is_new_merchant = True
            # genereate the merchant identifier
            post_merchant_id = uuid.uuid4()

        expense_json = {'identifier': uuid.uuid4(),
                        'amount': req_expense_amt,
                        'category_identifier': post_category_id,
                        'merchant_identifier': post_merchant_id,
                        'transaction_utc': req_transaction_utc}

        with get_dbclient().start_session() as session:
            with session.start_transaction():
                if is_new_category:
                    # insert the new category
                    category_object_id = self.db.categories.insert_one(
                        {'identifier': post_category_id,
                         'name': req_category_name}).inserted_id

                if is_new_merchant:
                    # insert the new merchant
                    merchant_object_id = self.db.merchants.insert_one(
                        {'identifier': post_merchant_id,
                         'name': req_merchant_name}).inserted_id

                # insert new expense
                expense_object_id = self.db.expenses.insert_one(
                    expense_json).inserted_id

        # return inserted record
        ret = self.db.expenses.find_one(expense_object_id)

        return {'message': 'Success', 'data': dumps(ret)}, 201


class Expense(Resource):
    def __init__(self):
        self.db = get_db()

    def get(self, identifier):

        expense = self.db.expenses.find_one(
            {'identifier': uuid.UUID(identifier)})

        if not expense:
            return {'message':
                    'Record not found for identifier: %s' % identifier}, 400

        return {'message': 'Success', 'data': dumps(expense)}, 200
