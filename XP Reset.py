import sqlite3

db = sqlite3.connect("users.db")

c = db.cursor()
c.execute("DELETE FROM users")
db.commit()
db.close()
