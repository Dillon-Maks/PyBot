import sqlite3
import time

conn = sqlite3.connect('/Users/dillonmaks/PycharmProjects/Discord\ Bot/users.db')
c = conn.cursor()
c.execute("UPDATE users SET DailyClaim=1 WHERE UserID=204808276397785088")
conn.commit()

token = 'NzMzNDY4ODA1Njk0NzUwNzQw.XxDmKQ.SAJEVE2YO6sXsZ5up7R6TinlYt8'
