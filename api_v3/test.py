import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

query = 'CREATE TABLE IF NOT EXISTS users (id int, username text, password text)'
cursor.execute(query)

create_user = 'INSERT INTO users VALUES (?, ?, ?)'
user = (1, 'anatolii', '123')
cursor.execute(create_user, user)

users = [
    (2, 'masha', '456'),
    (3, 'dasha', 'qwe')
]
cursor.executemany(create_user, users)

for row in cursor.execute('SELECT * FROM users'):
    print(row)


connection.commit()
connection.close()
