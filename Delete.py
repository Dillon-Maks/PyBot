import sqlite3

db = sqlite3.connect("users.db")
c = db.cursor()

c.execute("DELETE FROM users WHERE UserID=?", ["Æ Thrill#8228"])
db.commit()
db.close()