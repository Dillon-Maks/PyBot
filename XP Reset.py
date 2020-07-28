import sqlite3

db = sqlite3.connect("users.db")

c = db.cursor()
c.execute("UPDATE users SET Currency=10 WHERE UserID=277960322428698624")
db.commit()
db.close()
