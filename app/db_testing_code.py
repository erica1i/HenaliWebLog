import sqlite3

db_name = "test.db"

db = sqlite3.connect(db_name)
c =  db.cursor()

#c.execute("CREATE TABLE blogs (name TEXT, user_name TEXT, id INT PRIMARY KEY);")
c.execute("INSERT INTO blogs VALUES ('blog1', 'Foo', 1);")

db.commit()
db.close()
