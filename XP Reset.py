import sqlite3

db = sqlite3.connect("users.db")

c = db.cursor()
c.execute("UPDATE users SET Currency=50 WHERE Username='Maksimum#6716'")
db.commit()
db.close()
