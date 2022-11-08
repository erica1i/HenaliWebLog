import sqlite3

db_name = "test.db"

db = sqlite3.connect(db_name)
c =  db.cursor()
#DROP TABLE IF EXISTS users;
c.execute("CREATE TABLE users (name TEXT PRIMARY KEY, passwd TEXT);")
c.execute("CREATE TABLE blogs (name TEXT, user_name TEXT, id INTEGER PRIMARY KEY);")
c.execute("CREATE TABLE entries (contents TEXT, blog_id INT, id INTEGER PRIMARY KEY);")

db.commit()
db.close()
