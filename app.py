import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate
from security import identity
from db import db

from resources.user import UserRegister
from resources.item import Item
from resources.item import ItemList
from resources.store import Store
from resources.store import StoreList


app = Flask(__name__)
db_URL = 'sqlite:///data.db'
if (env_url := os.environ.get('DATABASE_URL')):
    split_url = env_url.split(':')
    split_url[0] = 'postgresql'
    db_URL = ':'.join(split_url)
app.config['SQLALCHEMY_DATABASE_URI'] = db_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'deFcon_11'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authentication_handler=authenticate, identity_handler=identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

db.init_app(app)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
