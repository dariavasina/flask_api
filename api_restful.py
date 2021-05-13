from flask import Flask, make_response, jsonify
from flask_restful import Resource, Api, reqparse


app = Flask(__name__)
api = Api(app)

items_list = [
    {
        'name': 'chair',
        'price': 1500
    }
]

if __name__ == '__main__':
    app.run(debug=True)


class Item(Resource):
    def get(self, name):
        item = list(filter(lambda x: x['name'] == name, items_list))
        if not item:
            return make_response("Error 404: item is not found", 404)
        return make_response(jsonify(item), 200)


    def post(self, name):
        item_in_list = list(filter(lambda x: x['name'] == name, items_list))
        if item_in_list:
            return make_response("Error: item already exists", 500)
        parser = reqparse.RequestParser()
        parser.add_argument('price', type=int)
        data = parser.parse_args()

        item = {
            'name': name,
            'price': data['price']

        }

        items_list.append(item)
        return make_response(item, 200)


    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('price', type=int)
        data = parser.parse_args()
        item_in_list = list(filter(lambda x: x['name'] == name, items_list))
        item = {
            'name': name,
            'price': data['price']
        }
        if item_in_list:
            n = items_list.index(item_in_list[0])
            items_list[n]['price'] = data['price']
            return make_response(item, 200)

        items_list.append(item)
        return make_response(item, 200)


    def delete(self, name):
        item = list(filter(lambda x: x['name'] == name, items_list))
        if item:
            n = items_list.index(item[0])
            item = {
                'name': name,
                'price': items_list[n]['price']
            }
            del items_list[n]
            return make_response(item, 200)

        return make_response("Eror 404: item is not found", 404)


class ItemList(Resource):
    def get(self):
        return make_response(jsonify(items_list), 200)


    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('items', type=dict, action='append')
        data = parser.parse_args()
        for i in range(len(data['items'])):
            if data['items'][i] in items_list:
                return make_response("Error: some of the items already exist", 500)
            items_list.append(data['items'][i])
        return make_response(jsonify(data['items']), 200)


api.add_resource(Item, '/items/<string:name>')
api.add_resource(ItemList, '/items')

