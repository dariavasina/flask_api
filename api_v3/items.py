from flask_jwt import jwt_required
from flask_restful import Resource, reqparse, abort
import sqlite3


def item_exists(name):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    query = 'SELECT name, price FROM store WHERE name=?'
    item = list(cursor.execute(query, (name,)).fetchone())
    connection.commit()
    connection.close()
    if item:
        return item
    return False


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price')

    @jwt_required()
    def get(self, name):
        if item_exists(name):
            item = item_exists(name)
            return {'name': name, 'price': item[1]}
        return abort(404, message='Item {} does not exist'.format(name))

    @jwt_required()
    def post(self, name):
        if item_exists(name):
            return abort(404, message='Item {} already exists'.format(name))

        price = Item.parser.parse_args()['price']
        try:
            price = int(price)
            item = {
                'name': name,
                'price': price
            }
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            query = 'INSERT INTO store VALUES (NULL, ?, ?)'
            cursor.execute(query, (name, price))
            connection.commit()
            connection.close()
            return {'new_item': item}, 200
        except:
            return {'message': "Parameter 'price' must be an integer"}

    @jwt_required()
    def put(self, name):
        price = Item.parser.parse_args()['price']
        try:
            price = int(price)
            item = {
                'name': name,
                'price': price
            }
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            if item_exists(name):
                query = 'UPDATE store SET price=? WHERE name=?'
                cursor.execute(query, (price, name))
                connection.commit()
                connection.close()
                return {'new_item': item}, 200
            query = 'INSERT INTO store VALUES (NULL, ?, ?)'
            cursor.execute(query, (name, price))
            connection.commit()
            connection.close()
            return {'new_item': item}, 200
        except:
            return {'message': "Parameter 'price' must be an integer"}

    @jwt_required()
    def delete(self, name):
        if item_exists(name):
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            query = 'DELETE FROM store WHERE name=?'
            cursor.execute(query, (name,))
            connection.commit()
            connection.close()
            return {'message': 'Successfully deleted item'}, 200
        return abort(404, message='Item {} does not exist'.format(name))


class ItemList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('items', type=dict, action='append')

    @jwt_required()
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'SELECT name, price FROM store'
        items_list = [{'name': row[0], 'price': row[1]} for row in cursor.execute(query)]
        connection.close()
        return {'items': items_list}

    @jwt_required()
    def post(self):
        new_items = []
        items = ItemList.parser.parse_args()['items']
        if items:
            for item in items:
                if item_exists(item['name']):
                    return abort(404, message='Item {} already exists'.format(item['price']))
                try:
                    item['price'] = int(item['price'])
                    new_items.append(item)
                except:
                    abort(400, message="Parameter 'price' must be an integer")

            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            query = 'INSERT INTO store VALUES (NULL, ?, ?)'
            cursor.executemany(query, [(item['name'], item['price']) for item in new_items])
            connection.commit()
            connection.close()
        return {'new_items': new_items}, 200

    @jwt_required()
    def delete(self):
        items = ItemList.parser.parse_args()['items']
        if items:
            for item in items:
                Item.delete(item['name'])
            return {'message': 'Successfully deleted items'}, 200
        return {'message': "List of items can't be empty"}, 400
