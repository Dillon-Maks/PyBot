import sqlite3

db = sqlite3.connect("users.db")

c = db.cursor()
c.execute("UPDATE users SET XP=90 WHERE UserID='Maksimum#6716'")
c.execute("UPDATE users SET Level=0 WHERE UserID='Maksimum#6716'")
db.commit()
db.close()
