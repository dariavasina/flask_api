import sqlite3
from flask_restful import Resource, reqparse, abort
from flask_jwt import jwt_required


def user_exists(username):
    if User.find_by_username(username) is not None:
        return True
    return False


class User(object):
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

    @staticmethod
    def find_by_username(name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'SELECT * FROM users WHERE username=?'
        row = cursor.execute(query, (name,)).fetchone()
        connection.close()
        user = User(*row) if row else None
        return user

    @staticmethod
    def find_by_id(_id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'SELECT * FROM users WHERE id=?'
        row = cursor.execute(query, (_id,)).fetchone()
        connection.close()
        user = User(*row) if row else None
        return user


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username')
    parser.add_argument('password')

    @jwt_required()
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'SELECT username, password FROM users'
        users = [{'username': row[0], 'password': row[1]} for row in cursor.execute(query)]
        connection.close()
        return {'users': users}

    def post(self):
        username = UserRegister.parser.parse_args()['username']
        password = UserRegister.parser.parse_args()['password']
        if user_exists(username):
            return abort(400, message="User '{}' already exists".format(username))
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'INSERT INTO users VALUES (?, ?)'
        cursor.execute(query, (username, password))
        connection.commit()
        connection.close()
        return {'username': username, 'password': password}

    @jwt_required()
    def put(self):
        new_user = {'username': UserRegister.parser.parse_args()['username'],
                    'password': UserRegister.parser.parse_args()['password']}
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        if user_exists(new_user['username']):
            query = 'UPDATE users SET password = ? WHERE username = ?'
            cursor.execute(query, (new_user['password'], new_user['username']))
            connection.commit()
            connection.close()
            return new_user, 200
        query = 'INSER INTO users VALUES (NULL, ?, ?)'
        cursor.execute(query, (new_user['password'], new_user['username']))
        connection.commit()
        connection.close()
        return new_user, 200

    @jwt_required()
    def delete(self):
        username = UserRegister.parser.parse_args()['username']
        if not user_exists(username):
            return abort(400, message="User '{}' already exists".format(username))
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'DELETE FROM users WHERE username=?'
        cursor.execute(query, (username,))
        connection.commit()
        connection.close()
        return 'Successfully deleted item', 200