import sqlite3
import random
from discord.ext import commands

client = commands.Bot(command_prefix='*')
conn = sqlite3.connect('users.db')

c = conn.cursor()

@client.event
async def on_ready():
    print('{0.user} is connected'.format(client))

@client.event
async def on_message(ctx):
    c.execute("SELECT * FROM users WHERE UserID=?", [str(ctx.author)])
    user = c.fetchone()
    if user[0] != str(client.user):
        if user is None:
            c.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (str(ctx.author), 0, 1, 0))
            conn.commit()
            c.execute("SELECT * FROM users WHERE UserID=?", [str(ctx.author)])
            user = c.fetchone()
        newXP = user[2] + random.randrange(1, 3)

        if newXP > round(100 * pow(user[1], 1.2)):
            currentLvl = user[1] + 1
            c.execute("UPDATE users SET Level=? Where UserID=?", (currentLvl, str(ctx.author)))
            conn.commit()
        elif newXP < 100:
            c.execute("UPDATE users set Level=1 WHERE UserID=?", [str(ctx.author)])
            conn.commit()

        c.execute("UPDATE users SET XP=? WHERE UserID=?", (newXP, str(ctx.author)))
        conn.commit()
        await client.process_commands(ctx)

@client.command()
async def xpcheck(ctx):
    c.execute("SELECT * FROM users WHERE UserID=?", [str(ctx.author)])
    user = c.fetchone()
    await ctx.send("Level: " + str(user[1]) + "\n" + str(user[2]) + "/" + str(round(100 * pow(user[1], 1.2))))


client.run('NzMzNDY4ODA1Njk0NzUwNzQw.XxDmKQ.SAJEVE2YO6sXsZ5up7R6TinlYt8')





