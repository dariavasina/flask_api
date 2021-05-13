from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from api_v3.security import authenticate, identity
from api_v3.items import Item, ItemList
from api_v3.users import User, UserRegister

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/items/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
