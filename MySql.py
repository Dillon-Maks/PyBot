import sqlite3


conn = sqlite3.connect('users.db')

c = conn.cursor()

# c.execute("""CREATE TABLE users (
#            UserID text,
#            Level integer,
#            XP integer,
#            Currency integer
#            )""")
# c.execute("INSERT INTO users VALUES ('Maksimum#6716', 0, 0, 0)")

c.execute("SELECT * FROM users WHERE UserID='Maksimum#6716'")
print(c.fetchone())

conn.commit()
conn.close()