import sqlite3

db_name = "test.db"

db = sqlite3.connect(db_name)
c =  db.cursor()

c.execute("CREATE TABLE users (name TEXT PRIMARY KEY, passwd TEXT);")

c.execute("CREATE TABLE blogs (user_name TEXT, user TEXT, id INT PRIMARY KEY);")

c.execute("CREATE TABLE entries (contents TEXT, blog_id INT, id INT PRIMARY KEY);")

db.commit()
db.close()