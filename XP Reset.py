import sqlite3

db = sqlite3.connect("users.db")

c = db.cursor()
c.execute("UPDATE users SET Currency=10 WHERE UserID=204808276397785088")
db.commit()
db.close()
