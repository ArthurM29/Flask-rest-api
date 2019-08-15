from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from Section5_SQLLite.src.security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'artie'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # creates new endpoint: /auth

items = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='This field cannot be left blank!')

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda it: it['name'] == name, items), None)  # next returns None if filtered is empty
        return {'item': item}, 200 if item else 404

    @jwt_required()
    def post(self, name):
        if next(filter(lambda it: it['name'] == name, items), None):
            return {'message': f"An item with name {name} already exists"}, 400

        payload = Item.parser.parse_args()
        item = {
            'name': name,
            'price': payload['price']
        }
        items.append(item)
        return item, 201

    @jwt_required()
    def delete(self, name):
        global items
        items = list(filter(lambda it: it['name'] != name, items))
        return {'message': 'Item deleted'}

    @jwt_required()
    def put(self, name):
        payload = Item.parser.parse_args()

        item = next(filter(lambda it: it['name'] == name, items), None)
        if not item:
            item = {
                'name': name,
                'price': payload['price']
            }
            items.append(item)
        else:
            item.update(payload)
        return item


class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(debug=True)
