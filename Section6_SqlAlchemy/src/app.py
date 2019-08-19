from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from Section5_SQLLite.src.security import authenticate, identity
from Section5_SQLLite.src.user import UserRegister
from Section5_SQLLite.src.item import Item, ItemList

app = Flask(__name__)
app.secret_key = 'artie'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # creates new endpoint: /auth

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(debug=True)
