import schedule
import sqlite3
import time

print("Running...")

conn = sqlite3.connect('users.db')
c = conn.cursor()

def dailyUpdate():
    c.execute("UPDATE users SET DailyClaim=1")
    conn.commit()
    print('Daily Claim Available!')

schedule.every().day.at("10:00").do(dailyUpdate)

while True:
    schedule.run_pending()
    time.sleep(5)