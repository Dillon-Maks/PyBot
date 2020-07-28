import sqlite3
from discord.ext import commands
from discord.utils import find

client = commands.Bot(command_prefix='*')
conn = sqlite3.connect('users.db')

c = conn.cursor()

@client.event
async def on_ready():
    print('{0.user} is connected'.format(client))

@client.event
async def on_member_join(member):
    c.execute("SELECT * FROM users WHERE UserID=?", [str(member)])
    user = c.fetchall()
    if user is None:
        c.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (str(member), 1, 0, 0))
        conn.commit()
    dm = client.get_user(member.id)
    await dm.send("Welcome to the server!")

@client.event
async def on_guild_join(guild):
    general = find(lambda x: x.name == 'general',  guild.text_channels)
    welcome = find(lambda x: x.name == 'welcome', guild.text_channels)
    rules = find(lambda x: x.name == 'rules', guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send('PyBot is Here! Command Prefix is *')
    elif welcome:
        await welcome.send('PyBot is Here! Command Prefix is *!')
    elif rules:
        pass

@client.event
async def on_message(ctx):
    c.execute("SELECT * FROM users WHERE UserID=?", [str(ctx.author.id)])
    user = c.fetchone()
    if ctx.author != "PyBot#3261":
        if user is None:
            c.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (str(ctx.author.id), 1, 0, 0))
            conn.commit()
            c.execute("SELECT * FROM users WHERE UserID=?", [str(ctx.author.id)])
            user = c.fetchone()
        msgValue = round(pow(len(ctx.content), 0.35))
        newXP = user[2] + msgValue
        print(str(ctx.author) + " has gained " + str(msgValue) + "XP")

        if newXP >= round(100 * pow(user[1], 1.2)):
            currentLvl = user[1] + 1
            c.execute("UPDATE users SET Level=? Where UserID=?", (currentLvl, str(ctx.author.id)))
            conn.commit()
        elif newXP < 100:
            c.execute("UPDATE users set Level=1 WHERE UserID=?", [str(ctx.author.id)])
            conn.commit()

        c.execute("UPDATE users SET XP=? WHERE UserID=?", (newXP, str(ctx.author.id)))
        conn.commit()
        await client.process_commands(ctx)

@client.command()
async def xpcheck(ctx):
    c.execute("SELECT * FROM users WHERE UserID=?", [str(ctx.author.id)])
    user = c.fetchone()
    await ctx.send("Level: " + str(user[1]) + "\n" + str(user[2]) + "/" + str(round(100 * pow(user[1], 1.2))))


client.run('NzMzNDY4ODA1Njk0NzUwNzQw.XxDmKQ.SAJEVE2YO6sXsZ5up7R6TinlYt8')





