from flask import Flask, g
from flask_restful import Resource, Api
from expense_tracker.db_helper import db_helper
from expense_tracker.expense_helper import Expenses, Expense
from expense_tracker.category_helper import Categories, Category
from expense_tracker.merchant_helper import Merchants, Merchant
import os
import markdown

# Create an instance of Flask
app = Flask(__name__)
api = Api(app)


@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db_helper().close_db()


@app.route('/')
def index():
    with open(os.path.dirname(app.root_path)
              + '/README.md', 'r') as markdown_file:
        content = markdown_file.read()
        return markdown.markdown(content)


api.add_resource(Expenses, '/expenses')
api.add_resource(Categories, '/categories')
api.add_resource(Merchants, '/merchants')
api.add_resource(Expense, '/expenses/<string:identifier>')
api.add_resource(Category, '/categories/<string:identifier>')
api.add_resource(Merchant, '/merchants/<string:identifier>')
