import sqlite3

connection = sqlite3.connect('database.db')


with open('/home/stephan/development/projects/wegewart/wwapp/schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO users (first_name, last_name, mail) VALUES (?, ?, ?)", ('John', 'Doe', 'John@doe.com'))
cur.execute("INSERT INTO users (first_name, last_name, mail) VALUES (?, ?, ?)", ('Stephan', 'Schuster', 'John@doe.com'))

cur.execute("INSERT INTO path_entry (type, who, activity, note, created_by) VALUES (?, ?, ?, ?, ?)", ('Blau', 'Stephan', 'Kontrolle', 'Naegel vergessen', 1))
connection.commit()
connection.close()