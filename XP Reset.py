import sqlite3

db = sqlite3.connect("users.db")

c = db.cursor()
c.execute("DELETE FROM users WHERE UserID=733468805694750740")
db.commit()
db.close()
