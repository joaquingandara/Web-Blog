import sqlite3

connection = sqlite3.connect('database.db')#Open connection to database (It will be created if not exists)

with open('schema.sql') as f:
    connection.executescript(f.read())#Execute sql script (Can execute more than one)

cur = connection.cursor() #Create a cursor. Cursor are iteration objects.

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('First Post', 'Content for the first post')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Second Post', 'Content for the second post')
            )

connection.commit()
connection.close()