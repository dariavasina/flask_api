import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

query_users = 'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)'
query_store = 'CREATE TABLE IF NOT EXISTS store (id INTEGER PRIMARY KEY, name text, price integer)'
cursor.execute(query_users)
cursor.execute(query_store)


connection.commit()
connection.close()