# mkdir section5
# cd section5
# virtualenv venv - -python = python3
# source venv/bin/activate
# pip install Flask
# pip install Flask-RESTful
# pip install Flask-JWT

from security import authenticate, identity
from flask_jwt import JWT
from flask_restful import Api
from flask import Flask
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from db import db

# reqparse is part of Python

app = Flask(__name__)
# To allow flask propagating exception even if debug is set to false on app
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# this is dangerous - only for development purpose
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
app.secret_key = 'jose'
api = Api(app)

# uses SQL_ALCHEMY to create the database
# using Flask decorators


@app.before_first_request
def create_tables():
    db.create_all()


# Provides the endpoint /oauth which receives username and password and returns a JWT
# When a endpoint is called, it uses the `identity` function to validate if the user is valid
jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/items/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/stores/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)  # important to mention debug=True
