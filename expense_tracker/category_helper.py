from flask import Flask, g, request
from flask_restful import Resource, Api
from bson.json_util import dumps
from expense_tracker.db_helper import db_helper
import os
import markdown
import datetime
import uuid


class CategoryModel():
    def __init__(self, identifier, name):
        self.identifier = identifier
        self.name = name

    def __repr__(self):
        return '<CategoryModel(identifier={self.identifier!r})>'


class Categories(Resource):
    def __init__(self):
        self.db = db_helper().get_db()

    def get(self):
        categories = dumps(list(self.db.categories.find({})))
        return {'message': 'Success', 'data': categories}


class Category(Resource):
    def __init__(self):
        self.db = get_db()

    def get(self, identifier):

        category = self.db.categories.find_one(
            {'identifier': uuid.UUID(identifier)})

        if not category:
            return {'message':
                    'Record not found for identifier: %s' % identifier}, 400

        return {'message': 'Success', 'data': dumps(category)}, 200
