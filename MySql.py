import sqlite3
from discord.ext import commands

client = commands.Bot(command_prefix='*')
conn = sqlite3.connect('users.db')

c = conn.cursor()

@client.event
async def on_ready():
    print('{0.user} is connected'.format(client))

@client.command()
async def xpcheck(ctx):
    user = c.execute("SELECT * FROM users WHERE UserID=?", [str(ctx.author)])
    if user is None:
        c.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (str(ctx.author), 0, 0, 0))
        conn.commit()
        text = c.fetchone()
        await ctx.send(c.fetchone())
    else:
        text = c.fetchone()
        await ctx.send(str(text[2]))
    conn.commit()

client.run('NzMzNDY4ODA1Njk0NzUwNzQw.XxDmKQ.SAJEVE2YO6sXsZ5up7R6TinlYt8')





